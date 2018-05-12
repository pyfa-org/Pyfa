# noinspection PyPackageRequirements
import wx
from logbook import Logger
import threading
import uuid
import time
import config
import base64
import json
import os
import config
import webbrowser

import eos.db
import datetime
from eos.enum import Enum
from eos.saveddata.ssocharacter import SsoCharacter
import gui.globalEvents as GE
from service.server import StoppableHTTPServer, AuthHandler
from service.settings import EsiSettings

import wx
from requests import Session

pyfalog = Logger(__name__)

from urllib.parse import urlencode

# todo: reimplement Caching for calls
# from esipy.cache import FileCache
# file_cache = FileCache(cache_path)
# cache_path = os.path.join(config.savePath, config.ESI_CACHE)
#
# if not os.path.exists(cache_path):
#     os.mkdir(cache_path)
#

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
    CHAR_SKILLS = "/v4/characters/{character_id}/skills/" # prepend https://esi.evetech.net/
    CHAR_FITTINGS = "/v1/characters/{character_id}/fittings/"
    CHAR_DEL_FIT = "/v1/characters/{character_id}/fittings/{fitting_id}/"

class Servers(Enum):
    TQ = 0
    SISI = 1


class LoginMethod(Enum):
    SERVER = 0
    MANUAL = 1


class Esi(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Esi()

        return cls._instance

    def __init__(self):
        self.settings = EsiSettings.getInstance()

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        self.implicitCharacter = None

        # need these here to post events
        import gui.mainFrame  # put this here to avoid loop
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        if sso_url is None or sso_url == "":
            raise AttributeError("sso_url cannot be None or empty "
                                 "without app parameter")

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

    def delSsoCharacter(self, id):
        char = eos.db.getSsoCharacter(id, config.getClientSecret())

        # There is an issue in which the SSO character is not removed from any linked characters - a reference to the
        # sso character remains even though the SSO character is deleted which should have deleted the link. This is a
        # work around until we can figure out why. Manually delete SSOCharacter from all of it's characters
        for x in char.characters:
            x._Character__ssoCharacters.remove(char)
        eos.db.remove(char)
        wx.PostEvent(self.mainFrame, GE.SsoLogout(charID=id))

    def getSsoCharacters(self):
        chars = eos.db.getSsoCharacters(config.getClientSecret())
        return chars

    def getSsoCharacter(self, id):
        """
        Get character, and modify to include the eve connection
        """
        char = eos.db.getSsoCharacter(id, config.getClientSecret())
        if char is not None and char.esi_client is None:
            char.esi_client = Esi.genEsiClient()
            Esi.update_token(char, Esi.get_sso_data(char)) # don't use update_token on security directly, se still need to apply the values here

        eos.db.commit()
        return char


    def getSkills(self, id):
        char = self.getSsoCharacter(id)
        resp = self.get(char, ESIEndpoints.CHAR_SKILLS, character_id=char.characterID)
        # resp = self.check_response(char.esi_client.request(op))
        return resp.json()

    def getSecStatus(self, id):
        char = self.getSsoCharacter(id)
        resp = self.get(char, ESIEndpoints.CHAR, character_id=char.characterID)
        return resp.json()

    def getFittings(self, id):
        char = self.getSsoCharacter(id)
        resp = self.get(char, ESIEndpoints.CHAR_FITTINGS, character_id=char.characterID)
        return resp.json()

    def postFitting(self, id, json_str):
        # @todo: new fitting ID can be recovered from resp.data,
        char = self.getSsoCharacter(id)
        resp = self.post(char, ESIEndpoints.CHAR_FITTINGS, json_str, character_id=char.characterID)
        return resp.json()

    def delFitting(self, id, fittingID):
        char = self.getSsoCharacter(id)
        self.delete(char, ESIEndpoints.CHAR_DEL_FIT, character_id=char.characterID, fitting_id=fittingID)

    def check_response(self, resp):
        # if resp.status >= 400:
        #     raise EsiException(resp.status)
        return resp

    @staticmethod
    def get_sso_data(char):
        """ Little "helper" function to get formated data for esipy security
        """
        return {
            'access_token': char.accessToken,
            'refresh_token': config.cipher.decrypt(char.refreshToken).decode(),
            'expires_in': (char.accessTokenExpires - datetime.datetime.utcnow()).total_seconds()
        }

    @staticmethod
    def update_token(char, tokenResponse):
        """ helper function to update token data from SSO response """
        char.accessToken = tokenResponse['access_token']
        char.accessTokenExpires = datetime.datetime.fromtimestamp(time.time() + tokenResponse['expires_in'])
        if 'refresh_token' in tokenResponse:
            char.refreshToken = config.cipher.encrypt(tokenResponse['refresh_token'].encode())

    def login(self):
        serverAddr = None
        if self.settings.get('loginMode') == LoginMethod.SERVER:
            serverAddr = self.startServer()
        uri = self.getLoginURI(serverAddr)
        webbrowser.open(uri)
        wx.PostEvent(self.mainFrame, GE.SsoLoggingIn(login_mode=self.settings.get('loginMode')))

    def stopServer(self):
        pyfalog.debug("Stopping Server")
        self.httpd.stop()
        self.httpd = None

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

    def startServer(self):  # todo: break this out into two functions: starting the server, and getting the URI
        pyfalog.debug("Starting server")

        # we need this to ensure that the previous get_request finishes, and then the socket will close
        if self.httpd:
            self.stopServer()
            time.sleep(1)

        self.httpd = StoppableHTTPServer(('localhost', 0), AuthHandler)
        port = self.httpd.socket.getsockname()[1]
        self.serverThread = threading.Thread(target=self.httpd.serve, args=(self.handleServerLogin,))
        self.serverThread.name = "SsoCallbackServer"
        self.serverThread.daemon = True
        self.serverThread.start()

        return 'http://localhost:{}'.format(port)

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

    def handleLogin(self, ssoInfo):
        auth_response = json.loads(base64.b64decode(ssoInfo))

        res = self._session.get(
            self.oauth_verify,
            headers=self.get_oauth_header(auth_response['access_token'])
        )
        if res.status_code != 200:
            raise APIException(
                self.oauth_verify,
                res.status_code,
                res.json()
            )
        cdata = res.json()
        print(cdata)

        currentCharacter = self.getSsoCharacter(cdata['CharacterName'])

        if currentCharacter is None:
            currentCharacter = SsoCharacter(cdata['CharacterID'], cdata['CharacterName'], config.getClientSecret())

        Esi.update_token(currentCharacter, auth_response)

        eos.db.save(currentCharacter)
        wx.PostEvent(self.mainFrame, GE.SsoLogin(character=currentCharacter))

    # get (endpoint, char, data?)

    def handleServerLogin(self, message):
        if not message:
            raise Exception("Could not parse out querystring parameters.")

        if message['state'][0] != self.state:
            pyfalog.warn("OAUTH state mismatch")
            raise Exception("OAUTH State Mismatch.")

        pyfalog.debug("Handling SSO login with: {0}", message)

        self.handleLogin(message['SSOInfo'][0])

    def __before_request(self, ssoChar):
        if ssoChar.is_token_expired():
            json_response = self.refresh(ssoChar)
            # AFTER_TOKEN_REFRESH.send(**json_response)

        if ssoChar.accessToken is not None:
            self._session.headers.update(self.get_oauth_header(ssoChar.accessToken))

    def get(self, ssoChar, endpoint, *args, **kwargs):
        self.__before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._session.get("{}{}".format(esi_url, endpoint))

        # check for warnings, also status > 400


    def post(self, ssoChar, endpoint, json, *args, **kwargs):
        self.__before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._session.post("{}{}".format(esi_url, endpoint), data=json)

        # check for warnings, also status > 400

    def delete(self, ssoChar, endpoint, *args, **kwargs):
        self.__before_request(ssoChar)
        endpoint = endpoint.format(**kwargs)
        return self._session.delete("{}{}".format(esi_url, endpoint))

        # check for warnings, also status > 400

