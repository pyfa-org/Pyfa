# noinspection PyPackageRequirements
from collections import namedtuple

from logbook import Logger
import uuid
import time
import config
import base64
import secrets
import hashlib
import json
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError, JWTClaimsError
import os
import datetime
from service.const import EsiSsoMode, EsiEndpoints
from service.settings import EsiSettings, NetworkSettings

from datetime import timedelta
from requests_cache import CachedSession

from requests import Session
from urllib.parse import urlencode

pyfalog = Logger(__name__)

scopes = [
    'esi-skills.read_skills.v1',
    'esi-fittings.read_fittings.v1',
    'esi-fittings.write_fittings.v1'
]

ApiBase = namedtuple('ApiBase', ['sso', 'esi'])
supported_servers = {
    "Tranquility": ApiBase("login.eveonline.com", "esi.evetech.net"),
    "Singularity": ApiBase("sisilogin.testeveonline.com", "esi.evetech.net"),
    "Serenity": ApiBase("login.evepc.163.com", "esi.evepc.163.com")
}

class GenericSsoError(Exception):
    """ Exception used for generic SSO errors that aren't directly related to an API call
    """
    pass

class APIException(Exception):
    """ Exception for API related errors """

    def __init__(self, url, code, json_response):
        self.url = url
        self.status_code = code
        self.response = json_response
        super(APIException, self).__init__(str(self))


    def __str__(self):
        if 'error_description' in self.response:
            return 'HTTP Error %s: %s' % (self.status_code,
                                          self.response['error_description'])
        elif 'message' in self.response:
            return 'HTTP Error %s: %s' % (self.status_code,
                                          self.response['message'])
        return 'HTTP Error %s' % self.status_code


class EsiAccess:
    def __init__(self):
        self.settings = EsiSettings.getInstance()
        self.server_base: ApiBase = supported_servers[self.settings.get("server")]

        # session request stuff
        self._session = Session()
        self._basicHeaders = {
            'Accept': 'application/json',
            'User-Agent': (
                'pyfa v{}'.format(config.version)
            )
        }
        self._session.headers.update(self._basicHeaders)
        self._session.proxies = NetworkSettings.getInstance().getProxySettingsInRequestsFormat()

        # Set up cached session. This is only used for SSO meta data for now, but can be expanded to actually handle
        # various ESI caching (using ETag, for example) in the future
        cached_session = CachedSession(
            os.path.join(config.savePath, config.ESI_CACHE),
            backend="sqlite",
            cache_control=True,                # Use Cache-Control headers for expiration, if available
            expire_after=timedelta(days=1),    # Otherwise expire responses after one day
            stale_if_error=True,               # In case of request errors, use stale cache data if possible
        )
        cached_session.headers.update(self._basicHeaders)
        cached_session.proxies = NetworkSettings.getInstance().getProxySettingsInRequestsFormat()

        meta_call = cached_session.get("https://%s/.well-known/oauth-authorization-server" % self.server_base.sso)
        meta_call.raise_for_status()
        self.server_meta = meta_call.json()

        jwks_call = cached_session.get(self.server_meta["jwks_uri"])
        jwks_call.raise_for_status()
        self.jwks = jwks_call.json()

    @property
    def sso_url(self):
        return 'https://%s/v2' % self.server_base.sso

    @property
    def esi_url(self):
        return 'https://%s' % self.server_base.esi

    @property
    def oauth_authorize(self):
        return self.server_meta["authorization_endpoint"]

    @property
    def oauth_token(self):
        return self.server_meta["token_endpoint"]

    @property
    def client_id(self):
        return self.settings.get('clientID') or config.API_CLIENT_ID

    @staticmethod
    def update_token(char, tokenResponse):
        """ helper function to update token data from SSO response """
        char.accessToken = tokenResponse['access_token']
        char.accessTokenExpires = datetime.datetime.fromtimestamp(time.time() + tokenResponse['expires_in'])
        if 'refresh_token' in tokenResponse:
            char.refreshToken = config.cipher.encrypt(tokenResponse['refresh_token'].encode())

    def get_login_uri(self, redirect=None):
        self.state = str(uuid.uuid4())

        # Generate the PKCE code challenge
        self.code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32))
        m = hashlib.sha256()
        m.update(self.code_verifier)
        d = m.digest()
        code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")

        state_arg = {
            'mode': self.settings.get('loginMode'),
            'redirect': redirect,
            'state': self.state
        }

        args = {
            'response_type': 'code',
            'redirect_uri': config.SSO_CALLBACK,
            'client_id': self.client_id,
            'scope': ' '.join(scopes),
            'code_challenge': code_challenge,
            'code_challenge_method':  'S256',
            'state': base64.b64encode(bytes(json.dumps(state_arg), 'utf-8'))
        }

        return '%s?%s' % (
            self.oauth_authorize,
            urlencode(args)
        )

    def get_oauth_header(self, token):
        """ Return the Bearer Authorization header required in oauth calls

        :return: a dict with the authorization header
        """
        return {'Authorization': 'Bearer %s' % token}

    def auth(self, code):
        values = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            "code_verifier": self.code_verifier
        }

        res = self.token_call(values)
        json_res = res.json()

        decoded_jwt = self.validate_eve_jwt(json_res['access_token'])
        return json_res, decoded_jwt

    def refresh(self, ssoChar):
        # todo: properly handle invalid refresh token
        values = {
            "grant_type": "refresh_token",
            "refresh_token": config.cipher.decrypt(ssoChar.refreshToken).decode(),
            "client_id": self.client_id,
        }

        res = self.token_call(values)
        json_res = res.json()
        self.update_token(ssoChar, json_res)
        return json_res

    def token_call(self, values):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": self.server_base.sso,
        }

        res = self._session.post(
            self.server_meta["token_endpoint"],
            data=values,
            headers=headers,
        )

        if res.status_code != 200:
            raise APIException(
                self.server_meta["token_endpoint"],
                res.status_code,
                res.json()
            )

        return res

    def validate_eve_jwt(self, jwt_token):
        """Validate a JWT token retrieved from the EVE SSO.

        Ignores the `aud` claim in token due to avoid unexpected breaking
        changes to ESI.

        Args:
            jwt_token: A JWT token originating from the EVE SSO
        Returns
            dict: The contents of the validated JWT token if there are no
                  validation errors
        """

        try:
            jwk_sets = self.jwks["keys"]
        except KeyError as e:
            raise GenericSsoError("Something went wrong when retrieving the JWK set. The returned "
                  "payload did not have the expected key {}. \nPayload returned "
                  "from the SSO looks like: {}".format(e, self.jwks))

        jwk_set = next((item for item in jwk_sets if item["alg"] == "RS256"))

        try:
            return jwt.decode(
                jwt_token,
                jwk_set,
                algorithms=jwk_set["alg"],
                issuer=[self.server_base.sso, "https://%s" % self.server_base.sso],
                # ignore "aud" claim: https://tweetfleet.slack.com/archives/C30KX8UUX/p1648495011905969
                options={"verify_aud": False, "verify_exp": self.settings.get("enforceJwtExpiration")}
            )
        except ExpiredSignatureError as e:
            raise GenericSsoError("The JWT token has expired: {}".format(str(e)))
        except JWTError as e:
            raise GenericSsoError("The JWT signature was invalid: {}".format(str(e)))
        except JWTClaimsError as e:
            raise GenericSsoError("The issuer claim was not from login.eveonline.com or "
                "https://login.eveonline.com: {}".format(str(e)))

    def _before_request(self, ssoChar):
        self._session.headers.clear()
        self._session.headers.update(self._basicHeaders)
        if ssoChar is None:
            return

        if ssoChar.is_token_expired():
            pyfalog.info("Refreshing token for {}".format(ssoChar.characterName))
            self.refresh(ssoChar)

        if ssoChar.accessToken is not None:
            self._session.headers.update(self.get_oauth_header(ssoChar.accessToken))

    def _after_request(self, resp):
        if "warning" in resp.headers:
            pyfalog.warn("{} - {}".format(resp.headers["warning"], resp.url))

        if resp.status_code >= 400:
            raise APIException(
                resp.url,
                resp.status_code,
                resp.json()
            )

        return resp

    def get(self, ssoChar, endpoint, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.get("{}{}".format(self.esi_url, endpoint)))

    def post(self, ssoChar, endpoint, json, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.post("{}{}".format(self.esi_url, endpoint), data=json))

    def delete(self, ssoChar, endpoint, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.delete("{}{}".format(self.esi_url, endpoint)))

    # todo: move these off to another class which extends this one. This class should only handle the low level
    # authentication and
    def getDynamicItem(self, typeID, itemID):
        return self.get(None, EsiEndpoints.DYNAMIC_ITEM.value, type_id=typeID, item_id=itemID)

    def getSkills(self, char):
        return self.get(char, EsiEndpoints.CHAR_SKILLS.value, character_id=char.characterID)

    def getSecStatus(self, char):
        return self.get(char, EsiEndpoints.CHAR.value, character_id=char.characterID)

    def getFittings(self, char):
        return self.get(char, EsiEndpoints.CHAR_FITTINGS.value, character_id=char.characterID)

    def postFitting(self, char, json_str):
        # @todo: new fitting ID can be recovered from resp.data,
        return self.post(char, EsiEndpoints.CHAR_FITTINGS.value, json_str, character_id=char.characterID)

    def delFitting(self, char, fittingID):
        return self.delete(char, EsiEndpoints.CHAR_DEL_FIT.value, character_id=char.characterID, fitting_id=fittingID)
