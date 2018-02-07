# noinspection PyPackageRequirements
import wx
from logbook import Logger
import threading
import copy
import uuid
import time
import config
import base64
import json

import eos.db
from eos.enum import Enum
from eos.saveddata.ssocharacter import SsoCharacter
import gui.globalEvents as GE
from service.settings import CRESTSettings
from service.server import StoppableHTTPServer, AuthHandler
from service.pycrest.eve import EVE

from .esi_security_proxy import EsiSecurityProxy
from esipy import EsiClient, EsiApp
from esipy.cache import FileCache
import os
import logging


pyfalog = Logger(__name__)

server = "https://blitzmann.pythonanywhere.com"
cache_path = os.path.join(config.savePath, config.ESI_CACHE)

if not os.path.exists(cache_path):
    os.mkdir(cache_path)

file_cache = FileCache(cache_path)

esiRdy = threading.Event()


class Servers(Enum):
    TQ = 0
    SISI = 1


class CrestModes(Enum):
    IMPLICIT = 0
    USER = 1

from utils.timer import Timer



class EsiInitThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "EsiInitThread"

    def run(self):
        Crest.initEsiApp()


class Crest(object):
    clientIDs = {
        Servers.TQ  : 'f9be379951c046339dc13a00e6be7704',
        Servers.SISI: 'af87365240d644f7950af563b8418bad'
    }

    # @todo: move this to settings
    clientCallback = 'http://localhost:6461'
    clientTest = True

    _instance = None

    @classmethod
    def initEsiApp(cls):
        with Timer() as t:
            cls.esiapp = EsiApp(cache=None)

        with Timer() as t:
            cls.esi_v1 = cls.esiapp.get_v1_swagger
        with Timer() as t:
            cls.esi_v4 = cls.esiapp.get_v4_swagger

        esiRdy.set()

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
            cls._instance = Crest()

        return cls._instance

    @classmethod
    def restartService(cls):
        # This is here to reseed pycrest values when changing preferences
        # We first stop the server n case one is running, as creating a new
        # instance doesn't do this.
        if cls._instance.httpd:
            cls._instance.stopServer()
        cls._instance = Crest()
        cls._instance.mainFrame.updateCrestMenus(type=cls._instance.settings.get('mode'))
        return cls._instance

    def __init__(self):
        """
        A note on login/logout events: the character login events happen
        whenever a characters is logged into via the SSO, regardless of mod.
        However, the mode should be send as an argument. Similarily,
        the Logout even happens whenever the character is deleted for either
        mode. The mode is sent as an argument, as well as the umber of
        characters still in the cache (if USER mode)
        """

        prefetch = EsiInitThread()
        prefetch.daemon = True
        prefetch.start()

        self.settings = CRESTSettings.getInstance()
        self.scopes = ['characterFittingsRead', 'characterFittingsWrite']

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        self.eve_options = {
            'client_id': self.settings.get('clientID') if self.settings.get('mode') == CrestModes.USER else self.clientIDs.get(self.settings.get('server')),
            'api_key': self.settings.get('clientSecret') if self.settings.get('mode') == CrestModes.USER else None,
            'redirect_uri': self.clientCallback,
            'testing': self.isTestServer
        }

        # Base EVE connection that is copied to all characters
        self.eve = EVE(**self.eve_options)

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

    def delCrestCharacter(self, charID):
        char = eos.db.getSsoCharacter(charID)
        del self.charCache[char.ID]
        eos.db.remove(char)
        wx.PostEvent(self.mainFrame, GE.SsoLogout(type=CrestModes.USER, numChars=len(self.charCache)))

    def delAllCharacters(self):
        chars = eos.db.getSsoCharacters()
        for char in chars:
            eos.db.remove(char)
        self.charCache = {}
        wx.PostEvent(self.mainFrame, GE.SsoLogout(type=CrestModes.USER, numChars=0))

    def getSsoCharacters(self):
        chars = eos.db.getSsoCharacters(config.getClientSecret())
        return chars

    def getSsoCharacter(self, charID):
        """
        Get character, and modify to include the eve connection
        """
        char = eos.db.getSsoCharacter(charID, config.getClientSecret())
        if char.esi_client is None:
            char.esi_client = Crest.genEsiClient()
            char.esi_client.security.update_token(char.get_sso_data())
        return char

    def getFittings(self, charID):
        char = self.getSsoCharacter(charID)
        op = Crest.esi_v1.op['get_characters_character_id_fittings'](
            character_id=charID
        )
        resp = char.esi_client.request(op)
        return resp

    def postFitting(self, charID, json):
        # @todo: new fitting ID can be recovered from Location header,
        # ie: Location -> https://api-sisi.testeveonline.com/characters/1611853631/fittings/37486494/
        char = self.getSsoCharacter(charID)
        return char.eve.post('%scharacters/%d/fittings/' % (char.eve._authed_endpoint, char.ID), data=json)

    def delFitting(self, charID, fittingID):
        char = self.getSsoCharacter(charID)
        return char.eve.delete('%scharacters/%d/fittings/%d/' % (char.eve._authed_endpoint, char.ID, fittingID))

    def logout(self):
        """Logout of implicit character"""
        pyfalog.debug("Character logout")
        self.implicitCharacter = None
        wx.PostEvent(self.mainFrame, GE.SsoLogout(type=self.settings.get('mode')))

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
            currentCharacter.esi_client = Crest.genEsiClient(esisecurity)
            currentCharacter.update_token(auth_response)  # this also sets the esi security token

        eos.db.save(currentCharacter)

        wx.PostEvent(self.mainFrame, GE.SsoLogin(type=CrestModes.USER))  # todo: remove user / implicit authentication
