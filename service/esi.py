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

import eos.db
import datetime
from eos.enum import Enum
from eos.saveddata.ssocharacter import SsoCharacter
import gui.globalEvents as GE
from service.settings import CRESTSettings
from service.server import StoppableHTTPServer, AuthHandler

from .esi_security_proxy import EsiSecurityProxy
from esipy import EsiClient, EsiApp
from esipy.cache import FileCache

pyfalog = Logger(__name__)

cache_path = os.path.join(config.savePath, config.ESI_CACHE)

if not os.path.exists(cache_path):
    os.mkdir(cache_path)

file_cache = FileCache(cache_path)


class Servers(Enum):
    TQ = 0
    SISI = 1


class Esi(object):
    esiapp = None
    esi_v1 = None
    esi_v4 = None

    _instance = None

    @classmethod
    def initEsiApp(cls):
        cls.esiapp = EsiApp(cache=file_cache)
        cls.esi_v1 = cls.esiapp.get_v1_swagger
        cls.esi_v4 = cls.esiapp.get_v4_swagger

        # esiRdy.set()

    @classmethod
    def genEsiClient(cls, security=None):
        return EsiClient(
            security=EsiSecurityProxy(sso_url=config.ESI_AUTH_PROXY) if security is None else security,
            cache=file_cache,
            headers={'User-Agent': 'pyfa esipy'}
        )

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Esi()

        return cls._instance

    def __init__(self):
        Esi.initEsiApp()

        self.settings = CRESTSettings.getInstance()

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        self.implicitCharacter = None

        # The database cache does not seem to be working for some reason. Use
        # this as a temporary measure
        self.charCache = {}

        # need these here to post events
        import gui.mainFrame  # put this here to avoid loop
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    @property
    def isTestServer(self):
        return self.settings.get('server') == Servers.SISI

    def delSsoCharacter(self, id):
        char = eos.db.getSsoCharacter(id)
        eos.db.remove(char)

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
            char.esi_client.security.update_token(Esi.get_sso_data(char))
        return char

    def getSkills(self, id):
        char = self.getSsoCharacter(id)
        op = Esi.esi_v4.op['get_characters_character_id_skills'](character_id=char.characterID)
        resp = char.esi_client.request(op)
        return resp.data

    def getSecStatus(self, id):
        char = self.getSsoCharacter(id)
        op = Esi.esi_v4.op['get_characters_character_id'](character_id=char.characterID)
        resp = char.esi_client.request(op)
        return resp.data

    def getFittings(self, id):
        char = self.getSsoCharacter(id)
        op = Esi.esi_v1.op['get_characters_character_id_fittings'](character_id=char.characterID)
        resp = char.esi_client.request(op)
        return resp.data

    def postFitting(self, id, json_str):
        # @todo: new fitting ID can be recovered from resp.data,
        char = self.getSsoCharacter(id)
        op = Esi.esi_v1.op['post_characters_character_id_fittings'](
            character_id=char.characterID,
            fitting=json.loads(json_str)
        )
        resp = char.esi_client.request(op)
        return resp.data

    def delFitting(self, id, fittingID):
        char = self.getSsoCharacter(id)
        op = Esi.esi_v1.op['delete_characters_character_id_fittings_fitting_id'](
            character_id=char.characterID,
            fitting_id=fittingID
        )
        resp = char.esi_client.request(op)
        return resp.data

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
        if char.esi_client is not None:
            char.esi_client.security.update_token(tokenResponse)

    def stopServer(self):
        pyfalog.debug("Stopping Server")
        self.httpd.stop()
        self.httpd = None

    def startServer(self):
        pyfalog.debug("Starting server")

        # we need this to ensure that the previous get_request finishes, and then the socket will close
        if self.httpd:
            self.stopServer()
            time.sleep(1)

        self.state = str(uuid.uuid4())
        self.httpd = StoppableHTTPServer(('localhost', 0), AuthHandler)
        port = self.httpd.socket.getsockname()[1]

        esisecurity = EsiSecurityProxy(sso_url=config.ESI_AUTH_PROXY)

        uri = esisecurity.get_auth_uri(state=self.state, redirect='http://localhost:{}'.format(port))

        self.serverThread = threading.Thread(target=self.httpd.serve, args=(self.handleLogin,))
        self.serverThread.name = "SsoCallbackServer"
        self.serverThread.daemon = True
        self.serverThread.start()

        return uri

    def handleLogin(self, message):
        if not message:
            raise Exception("Could not parse out querystring parameters.")

        if message['state'][0] != self.state:
            pyfalog.warn("OAUTH state mismatch")
            raise Exception("OAUTH State Mismatch.")

        pyfalog.debug("Handling CREST login with: {0}", message)

        auth_response = json.loads(base64.b64decode(message['SSOInfo'][0]))

        # We need to preload the ESI Security object beforehand with the auth response so that we can use verify to
        # get character information
        # init the security object
        esisecurity = EsiSecurityProxy(sso_url=config.ESI_AUTH_PROXY)

        esisecurity.update_token(auth_response)

        # we get the character information
        cdata = esisecurity.verify()
        print(cdata)

        currentCharacter = self.getSsoCharacter(cdata['CharacterID'])

        if currentCharacter is None:
            currentCharacter = SsoCharacter(cdata['CharacterID'], cdata['CharacterName'], config.getClientSecret())
            currentCharacter.esi_client = Esi.genEsiClient(esisecurity)
            Esi.update_token(currentCharacter, auth_response)  # this also sets the esi security token

        eos.db.save(currentCharacter)

