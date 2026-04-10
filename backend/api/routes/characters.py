"""Character management routes — /characters"""

import asyncio

import eos.db
from fastapi import APIRouter, HTTPException

from backend.api.models.module import (
    CharacterFull,
    CharacterLite,
    SkillOut,
    SkillUpdate,
)

router = APIRouter()


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _char_to_lite(char) -> CharacterLite:
    is_esi = hasattr(char, 'ssoCharacters') and bool(char.ssoCharacters)
    return CharacterLite(
        characterID=char.ID,
        name=char.name,
        isESI=is_esi,
        isBuiltin=char.name in ("All 0", "All 5", "Realistic"),
    )


def _char_to_full(char) -> CharacterFull:
    skills = []
    try:
        for skill in char.skills:
            skills.append(SkillOut(
                skillID=skill.item.typeID,
                skillName=skill.item.name,
                level=skill.level,
            ))
    except Exception:
        pass
    lite = _char_to_lite(char)
    return CharacterFull(**lite.model_dump(), skills=skills)


@router.get("", response_model=list[CharacterLite])
async def list_characters():
    def _get():
        from service.character import Character as sChar
        chars = sChar.getInstance().getCharacterList()
        return [_char_to_lite(c) for c in chars]
    return await _exe(_get)


@router.get("/{char_id}", response_model=CharacterFull)
async def get_character(char_id: int):
    def _get():
        from service.character import Character as sChar
        char = sChar.getInstance().getCharacter(char_id)
        if char is None:
            raise HTTPException(status_code=404, detail=f"Character {char_id} not found")
        return _char_to_full(char)
    return await _exe(_get)


@router.put("/{char_id}/skill/{skill_id}", response_model=CharacterFull)
async def set_skill_level(char_id: int, skill_id: int, body: SkillUpdate):
    if not 0 <= body.level <= 5:
        raise HTTPException(status_code=422, detail="Skill level must be 0–5")

    def _set():
        from service.character import Character as sChar
        char = sChar.getInstance().getCharacter(char_id)
        if char is None:
            raise HTTPException(status_code=404, detail=f"Character {char_id} not found")
        sChar.getInstance().setSkillLevel(char_id, skill_id, body.level)
        return _char_to_full(eos.db.getCharacter(char_id))
    return await _exe(_set)
