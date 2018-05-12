# noinspection PyPackageRequirements
from logbook import Logger
import uuid
import time
import config

import datetime
from eos.enum import Enum
from eos.saveddata.ssocharacter import SsoCharacter
from service.settings import EsiSettings

from requests import Session
from urllib.parse import urlencode

pyfalog = Logger(__name__)

# todo: reimplement Caching for calls
# from esipy.cache import FileCache
# file_cache = FileCache(cache_path)
# cache_path = os.path.join(config.savePath, config.ESI_CACHE)
#
# if not os.path.exists(cache_path):
#     os.mkdir(cache_path)
#

# todo: move these over to getters that automatically determine which endpoint we use.
sso_url = "https://www.pyfa.io"  # "https://login.eveonline.com" for actual login
esi_url = "https://esi.tech.ccp.is"

oauth_authorize = '%s/oauth/authorize' % sso_url
oauth_token = '%s/oauth/token' % sso_url


class APIException(Exception):
    """ Exception for SSO related errors """

    def __init__(self, url, code, json_response):
        self.url = url
        self.status_code = code
        self.response = json_response
        super(APIException, self).__init__(str(self))

    def __str__(self):
        if 'error' in self.response:
            return 'HTTP Error %s: %s' % (self.status_code,
                                          self.response['error'])
        elif 'message' in self.response:
            return 'HTTP Error %s: %s' % (self.status_code,
                                          self.response['message'])
        return 'HTTP Error %s' % (self.status_code)


class ESIEndpoints(Enum):
    CHAR = "/v4/characters/{character_id}/"
    CHAR_SKILLS = "/v4/characters/{character_id}/skills/"
    CHAR_FITTINGS = "/v1/characters/{character_id}/fittings/"
    CHAR_DEL_FIT = "/v1/characters/{character_id}/fittings/{fitting_id}/"


# class Servers(Enum):
#     TQ = 0
#     SISI = 1

class EsiAccess(object):
    def __init__(self):
        if sso_url is None or sso_url == "":
            raise AttributeError("sso_url cannot be None or empty "
                                 "without app parameter")

        self.settings = EsiSettings.getInstance()

        self.oauth_authorize = '%s/oauth/authorize' % sso_url
        self.oauth_token = '%s/oauth/token' % sso_url

        # use ESI url for verify, since it's better for caching
        if esi_url is None or esi_url == "":
            raise AttributeError("esi_url cannot be None or empty")
        self.oauth_verify = '%s/verify/' % esi_url


        # session request stuff
        self._session = Session()
        self._session.headers.update({
            'Accept': 'application/json',
            'User-Agent': (
                'pyfa v{}'.format(config.version)
            )
        })

    def getSkills(self, char):
        return self.get(char, ESIEndpoints.CHAR_SKILLS, character_id=char.characterID)

    def getSecStatus(self, char):
        return self.get(char, ESIEndpoints.CHAR, character_id=char.characterID)

    def getFittings(self, char):
        return self.get(char, ESIEndpoints.CHAR_FITTINGS, character_id=char.characterID)

    def postFitting(self, char, json_str):
        # @todo: new fitting ID can be recovered from resp.data,
        return self.post(char, ESIEndpoints.CHAR_FITTINGS, json_str, character_id=char.characterID)

    def delFitting(self, char, fittingID):
        return self.delete(char, ESIEndpoints.CHAR_DEL_FIT, character_id=char.characterID, fitting_id=fittingID)

    @staticmethod
    def update_token(char, tokenResponse):
        """ helper function to update token data from SSO response """
        char.accessToken = tokenResponse['access_token']
        char.accessTokenExpires = datetime.datetime.fromtimestamp(time.time() + tokenResponse['expires_in'])
        if 'refresh_token' in tokenResponse:
            char.refreshToken = config.cipher.encrypt(tokenResponse['refresh_token'].encode())

    def getLoginURI(self, redirect=None):
        self.state = str(uuid.uuid4())

        args = {
            'state': self.state,
            'pyfa_version': config.version,
            'login_method': self.settings.get('loginMode'),
            'client_hash': config.getClientSecret()
        }

        if redirect is not None:
            args['redirect'] = redirect

        return '%s?%s' % (
            oauth_authorize,
            urlencode(args)
        )

    def get_oauth_header(self, token):
        """ Return the Bearer Authorization header required in oauth calls

        :return: a dict with the authorization header
        """
        return {'Authorization': 'Bearer %s' % token}

    def get_refresh_token_params(self, refreshToken):
        """ Return the param object for the post() call to get the access_token
        from the refresh_token

        :param code: the refresh token
        :return: a dict with the url, params and header
        """
        if refreshToken is None:
            raise AttributeError('No refresh token is defined.')

        return {
            'data': {
                'grant_type': 'refresh_token',
                'refresh_token': refreshToken,
            },
            'url': self.oauth_token,
        }

    def refresh(self, ssoChar):
        request_data = self.get_refresh_token_params(config.cipher.decrypt(ssoChar.refreshToken).decode())
        res = self._session.post(**request_data)
        if res.status_code != 200:
            raise APIException(
                request_data['url'],
                res.status_code,
                res.json()
            )
        json_res = res.json()
        self.update_token(ssoChar, json_res)
        return json_res

    def _before_request(self, ssoChar):
        if ssoChar.is_token_expired():
            pyfalog.info("Refreshing token for {}".format(ssoChar.characterName))
            self.refresh(ssoChar)

        if ssoChar.accessToken is not None:
            self._session.headers.update(self.get_oauth_header(ssoChar.accessToken))

    def _after_request(self, resp):
        if ("warning" in resp.headers):
            pyfalog.warn("{} - {}".format(resp.headers["warning"], resp.url))

        if resp.status_code >= 400:
            raise APIException(
                resp.url,
                resp.status_code,
                resp.json()
            )

        return resp

    def get(self, ssoChar, endpoint, *args, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.get("{}{}".format(esi_url, endpoint)))

        # check for warnings, also status > 400

    def post(self, ssoChar, endpoint, json, *args, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.post("{}{}".format(esi_url, endpoint), data=json))

        # check for warnings, also status > 400

    def delete(self, ssoChar, endpoint, *args, **kwargs):
        self._before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._after_request(self._session.delete("{}{}".format(esi_url, endpoint)))

        # check for warnings, also status > 400

