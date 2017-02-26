# noinspection PyPackageRequirements
import wx
from logbook import Logger
import threading
import copy
import uuid
import time

import eos.db
from eos.enum import Enum
from eos.saveddata.crestchar import CrestChar
import gui.globalEvents as GE
from service.settings import CRESTSettings
from service.server import StoppableHTTPServer, AuthHandler
from service.pycrest.eve import EVE

pyfalog = Logger(__name__)


class Servers(Enum):
    TQ = 0
    SISI = 1


class CrestModes(Enum):
    IMPLICIT = 0
    USER = 1


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

        self.settings = CRESTSettings.getInstance()
        self.scopes = ['characterFittingsRead', 'characterFittingsWrite']

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        # Base EVE connection that is copied to all characters
        self.eve = EVE(
                client_id=self.settings.get('clientID') if self.settings.get(
                        'mode') == CrestModes.USER else self.clientIDs.get(self.settings.get('server')),
                api_key=self.settings.get('clientSecret') if self.settings.get('mode') == CrestModes.USER else None,
                redirect_uri=self.clientCallback,
                testing=self.isTestServer
        )

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
        char = eos.db.getCrestCharacter(charID)
        del self.charCache[char.ID]
        eos.db.remove(char)
        wx.PostEvent(self.mainFrame, GE.SsoLogout(type=CrestModes.USER, numChars=len(self.charCache)))

    def delAllCharacters(self):
        chars = eos.db.getCrestCharacters()
        for char in chars:
            eos.db.remove(char)
        self.charCache = {}
        wx.PostEvent(self.mainFrame, GE.SsoLogout(type=CrestModes.USER, numChars=0))

    def getCrestCharacters(self):
        chars = eos.db.getCrestCharacters()
        # I really need to figure out that DB cache problem, this is ridiculous
        chars2 = [self.getCrestCharacter(char.ID) for char in chars]
        return chars2

    def getCrestCharacter(self, charID):
        """
        Get character, and modify to include the eve connection
        """
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
        return char.eve.get('%scharacters/%d/fittings/' % (char.eve._authed_endpoint, char.ID))

    def postFitting(self, charID, json):
        # @todo: new fitting ID can be recovered from Location header,
        # ie: Location -> https://api-sisi.testeveonline.com/characters/1611853631/fittings/37486494/
        char = self.getCrestCharacter(charID)
        return char.eve.post('%scharacters/%d/fittings/' % (char.eve._authed_endpoint, char.ID), data=json)

    def delFitting(self, charID, fittingID):
        char = self.getCrestCharacter(charID)
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
        if self.httpd:
            self.stopServer()
            time.sleep(1)
            # we need this to ensure that the previous get_request finishes, and then the socket will close
        self.httpd = StoppableHTTPServer(('localhost', 6461), AuthHandler)

        self.serverThread = threading.Thread(target=self.httpd.serve, args=(self.handleLogin,))
        self.serverThread.name = "CRESTServer"
        self.serverThread.daemon = True
        self.serverThread.start()

        self.state = str(uuid.uuid4())
        return self.eve.auth_uri(scopes=self.scopes, state=self.state)

    def handleLogin(self, message):
        if not message:
            raise Exception("Could not parse out querystring parameters.")

        if message['state'][0] != self.state:
            pyfalog.warn("OAUTH state mismatch")
            raise Exception("OAUTH State Mismatch.")

        pyfalog.debug("Handling CREST login with: {0}", message)

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

            pyfalog.debug("Got character info: {0}", info)

            self.implicitCharacter = CrestChar(info['CharacterID'], info['CharacterName'])
            self.implicitCharacter.eve = eve
            # self.implicitCharacter.fetchImage()

            wx.PostEvent(self.mainFrame, GE.SsoLogin(type=CrestModes.IMPLICIT))
        elif 'code' in message:
            eve = copy.deepcopy(self.eve)
            eve.authorize(message['code'][0])
            eve()
            info = eve.whoami()

            pyfalog.debug("Got character info: {0}", info)

            # check if we have character already. If so, simply replace refresh_token
            char = self.getCrestCharacter(int(info['CharacterID']))
            if char:
                char.refresh_token = eve.refresh_token
            else:
                char = CrestChar(info['CharacterID'], info['CharacterName'], eve.refresh_token)
                char.eve = eve
            self.charCache[int(info['CharacterID'])] = char
            eos.db.save(char)

            wx.PostEvent(self.mainFrame, GE.SsoLogin(type=CrestModes.USER))
