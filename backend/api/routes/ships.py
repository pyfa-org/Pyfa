"""Ship browsing routes — /ships"""

import asyncio

import eos.db
from fastapi import APIRouter, HTTPException
from logbook import Logger

from backend.api.models.ship import AttributeOut, ShipFull, ShipLite

router = APIRouter()
pyfalog = Logger(__name__)

_ICON_BASE = "https://images.evetech.net/types/{typeID}/icon?size=64"
_RENDER_BASE = "https://images.evetech.net/types/{typeID}/render?size=128"

# EVE category ID for ships
_SHIP_CATEGORY_ID = 6


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _item_to_ship_lite(item) -> ShipLite:
    race_id = getattr(item, 'raceID', None)
    return ShipLite(
        typeID=item.typeID,
        name=item.name,
        groupID=item.group.ID if item.group else 0,
        groupName=item.group.name if item.group else "",
        raceID=race_id,
        iconURL=_ICON_BASE.format(typeID=item.typeID),
        renderURL=_RENDER_BASE.format(typeID=item.typeID),
    )


def _build_attribute_list(item) -> list[AttributeOut]:
    attrs = []
    try:
        for attr_id, val in item.attributes.items():
            attr_meta = eos.db.getAttributeInfo(attr_id)
            if attr_meta is None:
                continue
            attrs.append(AttributeOut(
                attributeID=attr_id,
                name=attr_meta.name,
                displayName=attr_meta.displayName,
                value=float(val.value if hasattr(val, 'value') else val),
                unit=str(attr_meta.unit.displayName) if attr_meta.unit else None,
                highIsGood=attr_meta.highIsGood,
            ))
    except Exception as exc:
        pyfalog.warning("Error building attributes for {0}: {1}", getattr(item, 'typeID', '?'), exc)
    return attrs


@router.get("", response_model=list[ShipLite])
async def list_ships():
    """List all published ships, grouped by race/class in the response."""
    def _get():
        from service.market import Market
        ships = Market.getInstance().getShipList()
        return [_item_to_ship_lite(s) for s in ships]
    return await _exe(_get)


@router.get("/search", response_model=list[ShipLite])
async def search_ships(q: str):
    def _search():
        from service.market import Market
        results = Market.getInstance().searchShips(q)
        return [_item_to_ship_lite(s) for s in results]
    return await _exe(_search)


@router.get("/{type_id}", response_model=ShipFull)
async def get_ship(type_id: int):
    def _get():
        item = eos.db.getItem(type_id)
        if item is None or item.category.ID != _SHIP_CATEGORY_ID:
            raise HTTPException(status_code=404, detail=f"Ship typeID {type_id} not found")

        lite = _item_to_ship_lite(item)

        # Slot counts via ship attributes
        def slot_count(attr_name):
            val = item.attributes.get(attr_name)
            if val is None:
                return 0
            return int(val.value if hasattr(val, 'value') else val)

        return ShipFull(
            **lite.model_dump(),
            description=item.description,
            attributes=_build_attribute_list(item),
            highSlots=slot_count('hiSlots'),
            midSlots=slot_count('medSlots'),
            lowSlots=slot_count('lowSlots'),
            rigSlots=slot_count('rigSlots'),
            subsystemSlots=slot_count('maxSubSystems'),
        )
    return await _exe(_get)
