import copy
import uuid

from wx.lib.pubsub import pub

import eos.db
from eos.types import Crest as CrestUser
from service import pycrest
import service
from service.server import *
import config
import logging
import threading

logger = logging.getLogger(__name__)

class Crest():

    # @todo: move this to settings
    clientCallback = 'http://localhost:6461'
    clientTest = True

    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = Crest()

        return cls._instance

    def __init__(self):
        self.settings = service.settings.CRESTSettings.getInstance()
        self.scopes = ['characterFittingsRead', 'characterFittingsWrite']

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None
        self.httpdTimer = None

        # Base EVE connection that is copied to all characters
        self.eve = pycrest.EVE(
                        client_id=self.settings.get('clientID') if self.settings.get('mode') == 1 else config.clientID,
                        api_key=self.settings.get('clientSecret') if self.settings.get('mode') == 1 else None,
                        redirect_uri=self.clientCallback,
                        testing=self.clientTest)

        self.implicitCharacter = None
        pub.subscribe(self.handleLogin, 'sso_login')

    def delCrestCharacter(self, charID):
        char = eos.db.getCrestCharacter(charID)
        eos.db.remove(char)

    def getCrestCharacters(self):
        chars = eos.db.getCrestCharacters()
        for char in chars:
            if not hasattr(char, "eve"):
                char.eve = copy.copy(self.eve)
                # Give EVE instance refresh info. This allows us to set it
                # without actually making the request to authorize at this time.
                char.eve.temptoken_authorize(refresh_token=char.refresh_token)

        wx.CallAfter(pub.sendMessage, 'crest_delete', message=None)

        return chars

    def getCrestCharacter(self, charID):
        '''
        Get character, and modify to include the eve connection
        '''
        if self.settings.get('mode') == 0:
            if self.implicitCharacter.ID != charID:
                raise ValueError("CharacterID does not match currently logged in character.")
            return self.implicitCharacter

        char = eos.db.getCrestCharacter(charID)
        if char and not hasattr(char, "eve"):
            char.eve = copy.copy(self.eve)
            char.eve.temptoken_authorize(refresh_token=char.refresh_token)
        return char

    def getFittings(self, charID):
        char = self.getCrestCharacter(charID)
        return char.eve.get('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID)

    def postFitting(self, charID, json):
        char = self.getCrestCharacter(charID)
        res = char.eve._session.post('https://api-sisi.testeveonline.com/characters/%d/fittings/'%char.ID, data=json)
        return res

    def logout(self):
        logging.debug("Character logout")
        self.implicitCharacter = None
        wx.CallAfter(pub.sendMessage, 'logout_success', message=None)

    def stopServer(self):
        logging.debug("Stopping Server")
        self.httpd.stop()

    def startServer(self):
        logging.debug("Starting server")
        self.httpd = StoppableHTTPServer(('', 6461), AuthHandler)
        thread.start_new_thread(self.httpd.serve, ())

        # keep server going for only 60 seconds
        self.httpdTimer = threading.Timer(60, self.stopServer)
        self.httpdTimer.start()

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
            eve = copy.copy(self.eve)
            eve.temptoken_authorize(
                access_token=message['access_token'][0],
                expires_in=int(message['expires_in'][0])
            )
            self.ssoTimer = threading.Timer(int(message['expires_in'][0]), self.logout)
            self.ssoTimer.start()

            eve()
            info = eve.whoami()

            logger.debug("Got character info: %s" % info)

            self.implicitCharacter = CrestUser(info['CharacterID'], info['CharacterName'])
            self.implicitCharacter.eve = eve
            self.implicitCharacter.fetchImage()

            wx.CallAfter(pub.sendMessage, 'login_success', type=0)
        elif 'code' in message:
            eve = copy.copy(self.eve)
            eve.authorize(message['code'][0])
            eve()
            info = eve.whoami()

            logger.debug("Got character info: %s" % info)

            # check if we have character already. If so, simply replace refresh_token
            char = self.getCrestCharacter(int(info['CharacterID']))
            if char:
                char.refresh_token = eve.refresh_token
            else:
                char = CrestUser(info['CharacterID'], info['CharacterName'], eve.refresh_token)
                char.eve = eve
            eos.db.save(char)

            wx.CallAfter(pub.sendMessage, 'login_success', type=1)

