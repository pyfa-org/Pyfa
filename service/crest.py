import thread
import config
import logging
import threading
import copy
import uuid
import wx
import time

from wx.lib.pubsub import pub

import eos.db
from eos.enum import Enum
from eos.types import CrestChar
import service

logger = logging.getLogger(__name__)

class Servers(Enum):
    TQ = 0
    SISI = 1

class CrestModes(Enum):
    IMPLICIT = 0
    USER = 1

class Crest():

    clientIDs = {
        Servers.TQ: 'f9be379951c046339dc13a00e6be7704',
        Servers.SISI: 'af87365240d644f7950af563b8418bad'
    }

    # @todo: move this to settings
    clientCallback = 'http://localhost:6461'
    clientTest = True

    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = Crest()

        return cls._instance

    @classmethod
    def restartService(cls):
        # This is hear to reseed pycrest values when changing preferences
        # We first stop the server n case one is running, as creating a new
        # instance doesn't do this.
        cls._instance.stopServer()
        cls._instance = Crest()
        return cls._instance

    def __init__(self):
        print "init crest"
        self.settings = service.settings.CRESTSettings.getInstance()
        self.scopes = ['characterFittingsRead', 'characterFittingsWrite']

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        # Base EVE connection that is copied to all characters
        self.eve = service.pycrest.EVE(
            client_id=self.settings.get('clientID') if self.settings.get('mode') == CrestModes.USER else self.clientIDs.get(self.settings.get('server')),
            api_key=self.settings.get('clientSecret') if self.settings.get('mode') == CrestModes.USER else None,
            redirect_uri=self.clientCallback,
            testing=self.isTestServer
        )

        self.implicitCharacter = None

        # The database cache does not seem to be working for some reason. Use
        # this as a temporary measure
        self.charCache = {}
        pub.subscribe(self.handleLogin, 'sso_login')

    @property
    def isTestServer(self):
        return self.settings.get('server') == Servers.SISI

    def delCrestCharacter(self, charID):
        char = eos.db.getCrestCharacter(charID)
        eos.db.remove(char)
        wx.CallAfter(pub.sendMessage, 'crest_delete', message=None)

    def delAllCharacters(self):
        chars = eos.db.getCrestCharacters()
        for char in chars:
            eos.db.remove(char)
        self.charCache = {}
        wx.CallAfter(pub.sendMessage, 'crest_delete', message=None)

    def getCrestCharacters(self):
        chars = eos.db.getCrestCharacters()
        return chars

    def getCrestCharacter(self, charID):
        '''
        Get character, and modify to include the eve connection
        '''
        if self.settings.get('mode') == CrestModes.IMPLICIT:
            if self.implicitCharacter.ID != charID:
                raise ValueError("CharacterID does not match currently logged in character.")
            return self.implicitCharacter

        if charID in self.charCache:
            return self.charCache.get(charID)

        char = eos.db.getCrestCharacter(charID)
        if char and not hasattr(char, "eve"):
            char.eve = copy.deepcopy(self.eve)
            char.eve.temptoken_authorize(refresh_token=char.refresh_token)
        self.charCache[charID] = char
        return char

    def getFittings(self, charID):
        char = self.getCrestCharacter(charID)
        return char.eve.get('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID)

    def postFitting(self, charID, json):
        char = self.getCrestCharacter(charID)
        return char.eve.post('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID, data=json)

    def delFitting(self, charID, fittingID):
        char = self.getCrestCharacter(charID)
        return char.eve.delete('https://api-sisi.testeveonline.com/characters/%d/fittings/%d/'%(char.ID, fittingID))

    def logout(self):
        logging.debug("Character logout")
        self.implicitCharacter = None
        wx.CallAfter(pub.sendMessage, 'logout_success', message=None)

    def stopServer(self):
        logging.debug("Stopping Server")
        self.httpd.stop()
        self.httpd = None

    def startServer(self):
        logging.debug("Starting server")
        if self.httpd:
            self.stopServer()
            time.sleep(1)  # we need this to ensure that the previous get_request finishes, and then the socket will close
        self.httpd = service.StoppableHTTPServer(('', 6461), service.AuthHandler)
        thread.start_new_thread(self.httpd.serve, ())

        self.state = str(uuid.uuid4())
        return self.eve.auth_uri(scopes=self.scopes, state=self.state)

    def handleLogin(self, message):
        if not message:
            return

        if message['state'][0] != self.state:
            logger.warn("OAUTH state mismatch")
            return

        logger.debug("Handling CREST login with: %s"%message)

        if 'access_token' in message:  # implicit
            eve = copy.deepcopy(self.eve)
            eve.temptoken_authorize(
                access_token=message['access_token'][0],
                expires_in=int(message['expires_in'][0])
            )
            self.ssoTimer = threading.Timer(int(message['expires_in'][0]), self.logout)
            self.ssoTimer.start()

            eve()
            info = eve.whoami()

            logger.debug("Got character info: %s" % info)

            self.implicitCharacter = CrestChar(info['CharacterID'], info['CharacterName'])
            self.implicitCharacter.eve = eve
            #self.implicitCharacter.fetchImage()

            wx.CallAfter(pub.sendMessage, 'login_success', type=CrestModes.IMPLICIT)
        elif 'code' in message:
            eve = copy.deepcopy(self.eve)
            eve.authorize(message['code'][0])
            eve()
            info = eve.whoami()

            logger.debug("Got character info: %s" % info)

            # check if we have character already. If so, simply replace refresh_token
            char = self.getCrestCharacter(int(info['CharacterID']))
            if char:
                char.refresh_token = eve.refresh_token
            else:
                char = CrestChar(info['CharacterID'], info['CharacterName'], eve.refresh_token)
                char.eve = eve
            self.charCache[int(info['CharacterID'])] = char
            eos.db.save(char)

            wx.CallAfter(pub.sendMessage, 'login_success', type=CrestModes.USER)

        self.stopServer()
