"""
Mobile ESI service — replaces service/esi.py for the mobile backend.

wx is gone entirely.  The key changes from the desktop version:

  - login() / SsoLogin dialog replaced by initOAuth() + handleCallback()
  - wx.PostEvent / wx.CallAfter replaced by plain Python callbacks
  - The StoppableHTTPServer OAuth callback listener is removed; the mobile
    app receives the deep-link redirect and POSTs code+state to the API
  - Token validation still runs on a background thread; the callback is an
    optional plain callable, not a wx event

OAuth flow (Section 7 of spec):
  1. App calls POST /characters/esi/init
  2. Backend generates PKCE verifier + state, returns authUrl
  3. App opens authUrl in system browser (expo-web-browser)
  4. CCP redirects to pyfa-mobile://esi-callback?code=...&state=...
  5. App POSTs code+state to POST /characters/esi/callback
  6. Backend calls handleCallback(code, state) here
"""

import base64
import json
import secrets
import threading
import time
from typing import Callable, Optional

import config
import eos.db
from logbook import Logger
from service.esiAccess import APIException, EsiAccess, GenericSsoError
from service.settings import EsiSettings
from eos.saveddata.ssocharacter import SsoCharacter

pyfalog = Logger(__name__)


class EsiTokenValidationThread(threading.Thread):
    """
    Background thread that checks all stored SSO tokens and refreshes
    any that are expired.  Identical logic to the desktop version but with
    wx.CallAfter replaced by a plain Python callback.
    """

    def __init__(self, callback: Optional[Callable] = None):
        super().__init__(name="EsiTokenValidation", daemon=True)
        self.callback = callback
        self.running = True

    def run(self):
        try:
            esi = MobileEsi.getInstance()
            chars = esi.getSsoCharacters()

            for char in chars:
                if not self.running:
                    return
                if char.is_token_expired():
                    pyfalog.info(f"Token expired for {char.characterName}, refreshing")
                    try:
                        esi.refresh(char)
                        eos.db.save(char)
                        pyfalog.info(f"Refreshed token for {char.characterName}")
                    except Exception as e:
                        pyfalog.error(f"Failed to refresh token for {char.characterName}: {e}")
        except Exception as e:
            pyfalog.error(f"Error in token validation thread: {e}")
        finally:
            if self.callback:
                self.callback()

    def stop(self):
        self.running = False


class MobileEsi(EsiAccess):
    """
    Mobile replacement for the desktop Esi class.

    Key differences from the desktop version
    ─────────────────────────────────────────
    • No wx imports anywhere
    • No local HTTP server — OAuth callback is received as a deep link
    • initOAuth() / handleCallback() replace login() / startServer()
    • PKCE (S256) is used for the code exchange
    • Token events are plain Python callbacks, not wx events
    """

    _instance: Optional["MobileEsi"] = None

    # Pending PKCE state: {state: code_verifier}
    _pending_states: dict[str, str] = {}

    @classmethod
    def getInstance(cls) -> "MobileEsi":
        if cls._instance is None:
            cls._instance = MobileEsi()
        return cls._instance

    def __init__(self):
        self.settings = EsiSettings.getInstance()
        super().__init__()

        self._on_login: Optional[Callable[[SsoCharacter], None]] = None
        self._on_logout: Optional[Callable[[int], None]] = None

        # Deleted fitting IDs (mirrors desktop behaviour)
        self.fittings_deleted: set[int] = set()

    # ------------------------------------------------------------------
    # Callbacks (set by the FastAPI startup or tests)
    # ------------------------------------------------------------------

    def setLoginCallback(self, fn: Callable[[SsoCharacter], None]):
        self._on_login = fn

    def setLogoutCallback(self, fn: Callable[[int], None]):
        self._on_logout = fn

    # ------------------------------------------------------------------
    # PKCE helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _generate_pkce_pair() -> tuple[str, str]:
        """Return (code_verifier, code_challenge) using S256 method."""
        import hashlib
        verifier = secrets.token_urlsafe(64)
        digest = hashlib.sha256(verifier.encode()).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
        return verifier, challenge

    # ------------------------------------------------------------------
    # OAuth flow
    # ------------------------------------------------------------------

    def initOAuth(self) -> tuple[str, str]:
        """
        Generate PKCE pair + state, build the CCP auth URL.

        Returns (auth_url, state).  The mobile app opens auth_url in the
        system browser; CCP redirects back to pyfa-mobile://esi-callback.
        """
        verifier, challenge = self._generate_pkce_pair()
        state = secrets.token_urlsafe(32)

        # Store verifier indexed by state for the callback
        MobileEsi._pending_states[state] = verifier

        params = {
            "response_type": "code",
            "redirect_uri": self.server_base.callback,
            "client_id": self.server_base.client_id,
            "scope": " ".join([
                "esi-skills.read_skills.v1",
                "esi-fittings.read_fittings.v1",
                "esi-fittings.write_fittings.v1",
                "publicData",
            ]),
            "state": base64.urlsafe_b64encode(
                json.dumps({"state": state}).encode()
            ).decode(),
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }

        from urllib.parse import urlencode
        auth_url = (
            f"https://{self.server_base.sso}/v2/oauth/authorize?{urlencode(params)}"
        )
        pyfalog.info("Generated ESI auth URL (state={})", state)
        return auth_url, state

    def handleCallback(self, code: str, state_enc: str) -> SsoCharacter:
        """
        Exchange the auth code for tokens.

        state_enc may be the raw state token or the base64-encoded JSON
        wrapper that CCP sends back ({"state": "<actual_state>"}).
        """
        # Decode the state wrapper CCP adds
        try:
            decoded = json.loads(base64.urlsafe_b64decode(state_enc + "=="))
            state = decoded["state"]
        except Exception:
            state = state_enc  # plain state (Serenity / tests)

        if state not in MobileEsi._pending_states:
            raise GenericSsoError(
                f"Unknown or expired OAuth state. Expected one of: "
                f"{list(MobileEsi._pending_states.keys())}"
            )

        verifier = MobileEsi._pending_states.pop(state)
        return self._exchangeCode(code, verifier)

    def _exchangeCode(self, code: str, verifier: str) -> SsoCharacter:
        """Perform the token exchange and persist the new SSO character."""
        auth_response, data = self.auth(code, code_verifier=verifier)

        sub_split = data["sub"].split(":")
        if len(sub_split) != 3:
            raise GenericSsoError(
                f"JWT sub does not contain expected data: {data['sub']}"
            )

        cid = sub_split[-1]
        char_name = data["name"]
        server_name = self.server_base.name

        current_char = self.getSsoCharacter(char_name, server_name)
        if current_char is None:
            current_char = SsoCharacter(
                cid, char_name, config.getClientSecret(), server_name
            )

        MobileEsi.update_token(current_char, auth_response)
        eos.db.save(current_char)
        eos.db.commit()

        pyfalog.info(f"ESI login successful for {char_name}")
        if self._on_login:
            self._on_login(current_char)

        return current_char

    # ------------------------------------------------------------------
    # Character management
    # ------------------------------------------------------------------

    def delSsoCharacter(self, char_id: int):
        char = eos.db.getSsoCharacter(char_id, config.getClientSecret())
        if char is None:
            return
        # Remove back-references (mirrors desktop workaround)
        for linked_char in char.characters:
            linked_char._Character__ssoCharacters.discard(char)
        eos.db.remove(char)
        eos.db.commit()
        pyfalog.info(f"Removed ESI character id={char_id}")
        if self._on_logout:
            self._on_logout(char_id)

    def getSsoCharacters(self):
        return eos.db.getSsoCharacters(config.getClientSecret())

    def getSsoCharacter(self, name_or_id, server=None):
        char = eos.db.getSsoCharacter(name_or_id, config.getClientSecret(), server)
        eos.db.commit()
        return char

    # ------------------------------------------------------------------
    # ESI data fetchers
    # ------------------------------------------------------------------

    def getSkills(self, char_id: int):
        char = self.getSsoCharacter(char_id)
        return super().getSkills(char).json()

    def getSecStatus(self, char_id: int):
        char = self.getSsoCharacter(char_id)
        return super().getSecStatus(char).json()

    def getFittings(self, char_id: int):
        char = self.getSsoCharacter(char_id)
        return super().getFittings(char).json()

    def postFitting(self, char_id: int, json_str: str):
        char = self.getSsoCharacter(char_id)
        return super().postFitting(char, json_str)

    def delFitting(self, char_id: int, fitting_id: int):
        char = self.getSsoCharacter(char_id)
        super().delFitting(char, fitting_id)
        self.fittings_deleted.add(fitting_id)

    # ------------------------------------------------------------------
    # Token refresh
    # ------------------------------------------------------------------

    def startTokenValidation(self, callback: Optional[Callable] = None):
        """Start the background token validation thread."""
        pyfalog.debug("Starting ESI token validation thread")
        thread = EsiTokenValidationThread(callback=callback)
        thread.start()
        return thread
