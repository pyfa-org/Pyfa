"""Market browsing routes — /market"""

import asyncio
from typing import Optional

import eos.db
from fastapi import APIRouter, HTTPException
from logbook import Logger

from backend.api.models.ship import AttributeOut, ItemFull, ItemLite

router = APIRouter()
pyfalog = Logger(__name__)

_ICON_BASE = "https://images.evetech.net/types/{typeID}/icon?size=64"

# EVE slot attribute IDs map to slot names
_SLOT_EFFECT_IDS = {
    11: "low",   # loPower
    12: "mid",   # medPower
    13: "high",  # hiPower
    2663: "rig",
    3772: "subsystem",
}


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _get_slot_from_item(item) -> Optional[str]:
    try:
        for effect in item.effects.values():
            slot = _SLOT_EFFECT_IDS.get(effect.effectID)
            if slot:
                return slot
    except Exception:
        pass
    return None


def _item_to_lite(item) -> ItemLite:
    return ItemLite(
        typeID=item.typeID,
        name=item.name,
        groupID=item.group.ID if item.group else 0,
        groupName=item.group.name if item.group else "",
        slot=_get_slot_from_item(item),
        iconURL=_ICON_BASE.format(typeID=item.typeID),
    )


def _build_attrs(item) -> list[AttributeOut]:
    attrs = []
    try:
        for attr_id, val in item.attributes.items():
            meta = eos.db.getAttributeInfo(attr_id)
            if meta is None:
                continue
            attrs.append(AttributeOut(
                attributeID=attr_id,
                name=meta.name,
                displayName=meta.displayName,
                value=float(val.value if hasattr(val, 'value') else val),
                unit=str(meta.unit.displayName) if meta.unit else None,
                highIsGood=meta.highIsGood,
            ))
    except Exception as exc:
        pyfalog.warning("Error building attrs: {0}", exc)
    return attrs


@router.get("/categories")
async def get_categories():
    """Return the full market category tree (categories → groups → items)."""
    def _get():
        from service.market import Market
        return Market.getInstance().getMarketTree()
    return await _exe(_get)


@router.get("/search", response_model=list[ItemLite])
async def search_market(q: str, slot: Optional[str] = None):
    def _search():
        from service.market import Market
        results = Market.getInstance().searchItems(q)
        items = [_item_to_lite(i) for i in results]
        if slot:
            items = [i for i in items if i.slot == slot]
        return items
    return await _exe(_search)


@router.get("/item/{type_id}", response_model=ItemFull)
async def get_item(type_id: int):
    def _get():
        item = eos.db.getItem(type_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item typeID {type_id} not found")
        lite = _item_to_lite(item)
        return ItemFull(
            **lite.model_dump(),
            description=item.description,
            attributes=_build_attrs(item),
        )
    return await _exe(_get)


@router.get("/item/{type_id}/variations", response_model=list[ItemLite])
async def get_variations(type_id: int):
    """Return T1/T2/faction/deadspace/officer variations for an item."""
    def _get():
        from service.market import Market
        item = eos.db.getItem(type_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item typeID {type_id} not found")
        variations = Market.getInstance().getVariations(item)
        return [_item_to_lite(v) for v in variations]
    return await _exe(_get)
