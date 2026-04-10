"""Price data routes — /prices"""

import asyncio
from typing import Optional

from fastapi import APIRouter

router = APIRouter()


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


@router.get("")
async def get_prices(typeIDs: str):
    """
    Batch price fetch for a comma-separated list of typeIDs.
    Returns a dict of {typeID: priceISK}.
    """
    try:
        ids = [int(x.strip()) for x in typeIDs.split(",") if x.strip()]
    except ValueError:
        return {}

    def _fetch():
        from service.price import Price
        return Price.getInstance().getPrices(ids)

    result = await _exe(_fetch)
    return result or {}
