import eos.db
from eos.types import Crest as CrestUser
import pycrest
import copy
import service
from service.server import *
import uuid
from gui.utils.repeatedTimer import RepeatedTimer

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

# TODO:
#     With implicit grant, make sure we know when it expires and delete/inactive char
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
        self.httpd = StoppableHTTPServer(('', 6461), AuthHandler)
        self.scopes = ['characterFittingsRead', 'characterFittingsWrite']
        self.state = None

        self.ssoTimer = RepeatedTimer(1, self.logout)

        # Base EVE connection that is copied to all characters
        self.eve = pycrest.EVE(
                        client_id=self.settings.get('clientID'),
                        api_key=self.settings.get('clientSecret') if self.settings.get('mode') == 1 else None,
                        redirect_uri=self.clientCallback,
                        testing=self.clientTest)

        self.implicitCharacter = None
        pub.subscribe(self.handleLogin, 'sso_login')

    def getCrestCharacters(self):
        chars = eos.db.getCrestCharacters()
        for char in chars:
            if not hasattr(char, "eve"):
                char.eve = copy.copy(self.eve)
                # Give EVE instance refresh info. This allows us to set it
                # without actually making the request to authorize at this time.
                char.eve.temptoken_authorize(refresh_token=char.refresh_token)
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
        if not hasattr(char, "eve"):
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

    def newChar(self, connection):
        connection()
        info = connection.whoami()
        char = CrestUser(info['CharacterName'], info['CharacterID'], connection.refresh_token)
        eos.db.save(char)

    def logout(self):
        self.implicitCharacter = None
        self.ssoTimer.stop()
        wx.CallAfter(pub.sendMessage, 'logout_success', message=None)

    def startServer(self):
        thread.start_new_thread(self.httpd.serve, ())
        self.state = str(uuid.uuid4())
        return self.eve.auth_uri(scopes=self.scopes, state=self.state)

    def handleLogin(self, message):
        if not message:
            return

        if message['state'][0] != self.state:
            print "state mismatch"
            return

        print "handling login by making characters and stuff"
        print message

        if 'access_token' in message:  # implicit
            eve = copy.copy(self.eve)
            eve.temptoken_authorize(
                access_token=message['access_token'][0],
                expires_in=int(message['expires_in'][0])
            )
            self.ssoTimer.interval = int(message['expires_in'][0])
            self.ssoTimer.start()

            eve()
            info = eve.whoami()
            self.implicitCharacter = CrestUser(info['CharacterID'], info['CharacterName'])
            self.implicitCharacter.eve = eve
            self.implicitCharacter.fetchImage()
            print self.implicitCharacter.eve, self.implicitCharacter.eve.refresh_token

            wx.CallAfter(pub.sendMessage, 'login_success', type=0)
        elif 'code' in message:
            print "handle authentication code"

            #wx.CallAfter(pub.sendMessage, 'login_success', type=1)



