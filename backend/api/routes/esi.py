"""
ESI OAuth routes — /characters/esi/...

Implements the mobile OAuth flow described in Section 7 of the spec:
  1. POST /characters/esi/init     → returns authUrl for system browser
  2. POST /characters/esi/callback → exchanges code+state for tokens
  3. DELETE /characters/esi/{id}   → removes ESI character
  4. POST /characters/esi/{id}/refresh → force token refresh
"""

import asyncio

import eos.db
from fastapi import APIRouter, HTTPException

from backend.api.models.module import (
    CharacterLite,
    EsiCallbackRequest,
    EsiInitResponse,
)

router = APIRouter()


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


@router.post("/init", response_model=EsiInitResponse)
async def esi_init():
    """
    Begin the ESI OAuth PKCE flow.

    Returns the URL the mobile app should open in the system browser via
    expo-web-browser openAuthSessionAsync().
    """
    def _init():
        from backend.service.esi import MobileEsi
        auth_url, state = MobileEsi.getInstance().initOAuth()
        return EsiInitResponse(authUrl=auth_url, state=state)
    return await _exe(_init)


@router.post("/callback", response_model=CharacterLite, status_code=201)
async def esi_callback(body: EsiCallbackRequest):
    """
    Handle the OAuth deep-link callback.

    The React Native app extracts code+state from the deep link URI
    (pyfa-mobile://esi-callback?code=...&state=...) and POSTs them here.
    """
    def _callback():
        from backend.service.esi import MobileEsi
        from backend.api.routes.characters import _char_to_lite
        char = MobileEsi.getInstance().handleCallback(body.code, body.state)
        return _char_to_lite(char)
    return await _exe(_callback)


@router.delete("/{sso_char_id}", status_code=204)
async def delete_esi_character(sso_char_id: int):
    def _delete():
        from backend.service.esi import MobileEsi
        MobileEsi.getInstance().delSsoCharacter(sso_char_id)
    await _exe(_delete)


@router.post("/{sso_char_id}/refresh", response_model=CharacterLite)
async def refresh_esi_token(sso_char_id: int):
    def _refresh():
        from backend.service.esi import MobileEsi
        from backend.api.routes.characters import _char_to_lite
        esi = MobileEsi.getInstance()
        char = eos.db.getSsoCharacter(sso_char_id, None)
        if char is None:
            raise HTTPException(status_code=404, detail=f"SSO character {sso_char_id} not found")
        esi.refresh(char)
        eos.db.save(char)
        return _char_to_lite(char)
    return await _exe(_refresh)
