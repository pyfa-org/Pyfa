"""
App settings, damage patterns, and target profile routes.
"""

import asyncio

import eos.db
from fastapi import APIRouter, HTTPException

from backend.api.models.module import (
    AppSettings,
    DamagePatternCreate,
    DamagePatternOut,
    TargetProfileCreate,
    TargetProfileOut,
)

router = APIRouter()


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


# ---------------------------------------------------------------------------
# App settings
# ---------------------------------------------------------------------------

@router.get("", response_model=AppSettings)
async def get_settings():
    def _get():
        from service.settings import SettingsProvider
        sp = SettingsProvider.getInstance()
        s = sp.getSettings("pyfaMobileSettings", {
            "useGlobalCharacter": False,
            "useGlobalDamagePattern": False,
        })
        return AppSettings(
            useGlobalCharacter=s["useGlobalCharacter"],
            useGlobalDamagePattern=s["useGlobalDamagePattern"],
        )
    return await _exe(_get)


@router.put("", response_model=AppSettings)
async def update_settings(body: AppSettings):
    def _set():
        from service.settings import SettingsProvider
        sp = SettingsProvider.getInstance()
        s = sp.getSettings("pyfaMobileSettings", {})
        for key, val in body.model_dump().items():
            s[key] = val
        s.save()
        return body
    return await _exe(_set)


# ---------------------------------------------------------------------------
# Damage patterns
# ---------------------------------------------------------------------------

def _pattern_to_out(p) -> DamagePatternOut:
    return DamagePatternOut(
        patternID=p.ID,
        name=p.name,
        em=p.emAmount,
        therm=p.thermalAmount,
        kin=p.kineticAmount,
        exp=p.explosiveAmount,
        isBuiltin=p.builtin,
    )


@router.get("/damage-patterns", response_model=list[DamagePatternOut])
async def list_damage_patterns():
    def _get():
        return [_pattern_to_out(p) for p in eos.db.getDamagePatternList()]
    return await _exe(_get)


@router.post("/damage-patterns", response_model=DamagePatternOut, status_code=201)
async def create_damage_pattern(body: DamagePatternCreate):
    def _create():
        from service.damagePattern import DamagePattern as sDmg
        p = sDmg.getInstance().newPattern(
            body.name, body.em, body.therm, body.kin, body.exp
        )
        return _pattern_to_out(p)
    return await _exe(_create)


@router.put("/damage-patterns/{pattern_id}", response_model=DamagePatternOut)
async def update_damage_pattern(pattern_id: int, body: DamagePatternCreate):
    def _update():
        p = eos.db.getDamagePattern(pattern_id)
        if p is None:
            raise HTTPException(status_code=404, detail=f"Pattern {pattern_id} not found")
        p.name = body.name
        p.emAmount = body.em
        p.thermalAmount = body.therm
        p.kineticAmount = body.kin
        p.explosiveAmount = body.exp
        eos.db.commit()
        return _pattern_to_out(p)
    return await _exe(_update)


@router.delete("/damage-patterns/{pattern_id}", status_code=204)
async def delete_damage_pattern(pattern_id: int):
    def _delete():
        from service.damagePattern import DamagePattern as sDmg
        p = eos.db.getDamagePattern(pattern_id)
        if p is None:
            raise HTTPException(status_code=404, detail=f"Pattern {pattern_id} not found")
        sDmg.getInstance().deletePattern(pattern_id)
    await _exe(_delete)


# ---------------------------------------------------------------------------
# Target profiles
# ---------------------------------------------------------------------------

def _profile_to_out(p) -> TargetProfileOut:
    return TargetProfileOut(
        profileID=p.ID,
        name=p.name,
        signatureRadius=p.signatureRadius,
        velocity=p.velocity,
        distance=p.distance,
        isBuiltin=p.builtin,
    )


@router.get("/target-profiles", response_model=list[TargetProfileOut])
async def list_target_profiles():
    def _get():
        return [_profile_to_out(p) for p in eos.db.getTargetProfileList()]
    return await _exe(_get)


@router.post("/target-profiles", response_model=TargetProfileOut, status_code=201)
async def create_target_profile(body: TargetProfileCreate):
    def _create():
        from service.targetProfile import TargetProfile as sTP
        p = sTP.getInstance().newProfile(
            body.name,
            body.signatureRadius,
            body.velocity,
            body.distance,
        )
        return _profile_to_out(p)
    return await _exe(_create)


@router.delete("/target-profiles/{profile_id}", status_code=204)
async def delete_target_profile(profile_id: int):
    def _delete():
        from service.targetProfile import TargetProfile as sTP
        p = eos.db.getTargetProfile(profile_id)
        if p is None:
            raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")
        sTP.getInstance().deleteProfile(profile_id)
    await _exe(_delete)
