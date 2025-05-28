# noinspection PyPackageRequirements
import wx
from logbook import Logger
import threading
import time
import base64
import json
import config
import re

import eos.db
from service.const import EsiLoginMethod, EsiSsoMode
from eos.saveddata.ssocharacter import SsoCharacter
from service.esiAccess import APIException, GenericSsoError
import gui.globalEvents as GE
from gui.ssoLogin import SsoLogin
from service.server import StoppableHTTPServer, AuthHandler
from service.settings import EsiSettings
from service.esiAccess import EsiAccess
import gui.mainFrame

from requests import Session

pyfalog = Logger(__name__)
_t = wx.GetTranslation


class Esi(EsiAccess):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = Esi()

        return cls._instance

    def __init__(self):
        self.settings = EsiSettings.getInstance()

        super().__init__()

        # these will be set when needed
        self.httpd = None
        self.state = None
        self.ssoTimer = None

        self.implicitCharacter = None

        # until I can get around to making proper caching and modifications to said cache, storee deleted fittings here
        # so that we can easily hide them in the fitting browser
        self.fittings_deleted = set()

        # need these here to post events
        import gui.mainFrame  # put this here to avoid loop
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

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

    def getSsoCharacter(self, id, server=None):
        char = eos.db.getSsoCharacter(id, config.getClientSecret(), server)
        eos.db.commit()
        return char

    def getSkills(self, id):
        char = self.getSsoCharacter(id)
        resp = super().getSkills(char)
        return resp.json()

    def getSecStatus(self, id):
        char = self.getSsoCharacter(id)
        resp = super().getSecStatus(char)
        return resp.json()

    def getFittings(self, id):
        char = self.getSsoCharacter(id)
        resp = super().getFittings(char)
        return resp.json()

    def postFitting(self, id, json_str):
        # @todo: new fitting ID can be recovered from resp.data,
        char = self.getSsoCharacter(id)
        resp = super().postFitting(char, json_str)
        return resp

    def delFitting(self, id, fittingID):
        char = self.getSsoCharacter(id)
        super().delFitting(char, fittingID)
        self.fittings_deleted.add(fittingID)

    def login(self):
        start_server = self.settings.get('loginMode') == EsiLoginMethod.SERVER and self.server_base.supports_auto_login
        with gui.ssoLogin.SsoLogin(self.server_base, start_server) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                from gui.esiFittings import ESIExceptionHandler

                try:
                    if self.server_name == "Serenity":
                        s = re.search(r'(?<=code=)[a-zA-Z0-9\-_]*', dlg.ssoInfoCtrl.Value.strip())
                        if s:
                            # skip state verification and go directly through the auth code processing
                            self.handleLogin(s.group(0))
                        else:
                            pass
                            # todo: throw error
                    else:
                        self.handleServerRequest(json.loads(base64.b64decode(dlg.ssoInfoCtrl.Value.strip())))
                except GenericSsoError as ex:
                    pyfalog.error(ex)
                    with wx.MessageDialog(
                            self.mainFrame,
                            str(ex),
                            _t("SSO Error"),
                            wx.OK | wx.ICON_ERROR
                    ) as dlg:
                        dlg.ShowModal()
                except APIException as ex:
                    pyfalog.error(ex)
                    ESIExceptionHandler(ex)
                    pass


    def stopServer(self):
        pyfalog.debug("Stopping Server")
        if self.httpd:
            self.httpd.stop()
            self.httpd = None

    def startServer(self, port):  # todo: break this out into two functions: starting the server, and getting the URI
        pyfalog.debug("Starting server")

        # we need this to ensure that the previous get_request finishes, and then the socket will close
        if self.httpd:
            self.stopServer()
            time.sleep(1)

        self.httpd = StoppableHTTPServer(('localhost', port), AuthHandler)
        port = self.httpd.socket.getsockname()[1]
        self.serverThread = threading.Thread(target=self.httpd.serve, args=(self.handleServerRequest,))
        self.serverThread.name = "SsoCallbackServer"
        self.serverThread.daemon = True
        self.serverThread.start()

        return 'http://localhost:{}'.format(port)

    def handleLogin(self, code):
        auth_response, data = self.auth(code)

        currentCharacter = self.getSsoCharacter(data['name'], self.server_base.name)

        sub_split = data["sub"].split(":")

        if len(sub_split) != 3:
            raise GenericSsoError("JWT sub does not contain the expected data. Contents: %s" % data["sub"])

        cid = sub_split[-1]
        if currentCharacter is None:
            currentCharacter = SsoCharacter(cid, data['name'], config.getClientSecret(), self.server_base.name)

        Esi.update_token(currentCharacter, auth_response)

        eos.db.save(currentCharacter)
        wx.PostEvent(self.mainFrame, GE.SsoLogin(character=currentCharacter))

    # get (endpoint, char, data?)

    def handleServerRequest(self, message):
        if not message:
            raise GenericSsoError("Could not parse out querystring parameters.")

        try:
            state_enc = message['state']
            state = json.loads(base64.b64decode(state_enc))['state']
        except Exception:
            raise GenericSsoError("There was a problem decoding state parameter.")

        if state != self.state:
            pyfalog.warn("OAUTH state mismatch")
            raise GenericSsoError("OAUTH State Mismatch.")

        pyfalog.debug("Handling SSO login with: {0}", message)

        self.handleLogin(message['code'])
