"""Character and damage-pattern Pydantic models."""

from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

class SkillOut(BaseModel):
    skillID: int
    skillName: str
    level: int


class CharacterLite(BaseModel):
    characterID: int
    name: str
    isESI: bool
    isBuiltin: bool


class CharacterFull(CharacterLite):
    skills: list[SkillOut]
    secStatus: Optional[float] = None


class SkillUpdate(BaseModel):
    level: int


class EsiInitResponse(BaseModel):
    authUrl: str
    state: str


class EsiCallbackRequest(BaseModel):
    code: str
    state: str


# ---------------------------------------------------------------------------
# Damage patterns and target profiles
# ---------------------------------------------------------------------------

class DamagePatternOut(BaseModel):
    patternID: int
    name: str
    em: float
    therm: float
    kin: float
    exp: float
    isBuiltin: bool


class DamagePatternCreate(BaseModel):
    name: str
    em: float
    therm: float
    kin: float
    exp: float


class TargetProfileOut(BaseModel):
    profileID: int
    name: str
    signatureRadius: Optional[float] = None
    velocity: Optional[float] = None
    distance: Optional[float] = None
    shieldResists: Optional[dict] = None
    armorResists: Optional[dict] = None
    hullResists: Optional[dict] = None
    isBuiltin: bool


class TargetProfileCreate(BaseModel):
    name: str
    signatureRadius: Optional[float] = None
    velocity: Optional[float] = None
    distance: Optional[float] = None


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class AppSettings(BaseModel):
    useGlobalCharacter: bool = False
    useGlobalDamagePattern: bool = False
    defaultCharacterID: Optional[int] = None
    defaultPatternID: Optional[int] = None
    priceProvider: str = "fuzzwork"
    language: str = "en"
