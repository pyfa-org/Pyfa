"""Pydantic models for ships and market items."""

from typing import Optional
from pydantic import BaseModel


class AttributeOut(BaseModel):
    attributeID: int
    name: str
    displayName: Optional[str] = None
    value: float
    unit: Optional[str] = None
    highIsGood: Optional[bool] = None


class ShipLite(BaseModel):
    typeID: int
    name: str
    groupID: int
    groupName: str
    raceID: Optional[int] = None
    raceName: Optional[str] = None
    iconURL: Optional[str] = None
    renderURL: Optional[str] = None


class ShipFull(ShipLite):
    description: Optional[str] = None
    attributes: list[AttributeOut]
    highSlots: int
    midSlots: int
    lowSlots: int
    rigSlots: int
    subsystemSlots: int


class MarketCategory(BaseModel):
    categoryID: int
    name: str
    groups: list["MarketGroup"]


class MarketGroup(BaseModel):
    groupID: int
    name: str
    items: list["ItemLite"]


class ItemLite(BaseModel):
    typeID: int
    name: str
    groupID: int
    groupName: str
    metaLevel: Optional[int] = None
    slot: Optional[str] = None
    iconURL: Optional[str] = None


class ItemFull(ItemLite):
    description: Optional[str] = None
    attributes: list[AttributeOut]
    variations: list[ItemLite] = []


MarketCategory.model_rebuild()
MarketGroup.model_rebuild()
