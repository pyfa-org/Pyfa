"""
Graph data routes — /graphs/...

Returns arrays of {x, y} data points consumed by Victory Native on the
React Native side.  The actual calculation is delegated to the existing
graphs/ module (kept unmodified as per spec Section 3.3).
"""

import asyncio
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DataPoint(BaseModel):
    x: float
    y: float


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _parse_ids(fit_ids_str: str) -> list[int]:
    """Parse comma-separated fit IDs."""
    try:
        return [int(x.strip()) for x in fit_ids_str.split(",") if x.strip()]
    except ValueError:
        return []


@router.get("/dps-range")
async def dps_vs_range(
    fitIDs: str,
    targetSig: Optional[float] = None,
    targetVelocity: Optional[float] = None,
):
    """DPS vs range graph data for one or more fits."""
    fit_ids = _parse_ids(fitIDs)

    def _compute():
        from graphs.graph import FitGraph
        results = {}
        for fit_id in fit_ids:
            try:
                graph = FitGraph.getInstance()
                points = graph.getPlotPoints(
                    fit_id,
                    "dpsRange",
                    xRange=(0, 100000),
                    xSteps=100,
                    extraParams={"targetSig": targetSig, "targetVelocity": targetVelocity},
                )
                results[fit_id] = [{"x": p[0], "y": p[1]} for p in points]
            except Exception:
                results[fit_id] = []
        return results

    return await _exe(_compute)


@router.get("/dps-time")
async def dps_vs_time(
    fitIDs: str,
    distance: Optional[float] = None,
):
    """DPS vs time graph (capacitor / reload cycles)."""
    fit_ids = _parse_ids(fitIDs)

    def _compute():
        from graphs.graph import FitGraph
        results = {}
        for fit_id in fit_ids:
            try:
                graph = FitGraph.getInstance()
                points = graph.getPlotPoints(
                    fit_id,
                    "dpsTime",
                    xRange=(0, 300),
                    xSteps=100,
                    extraParams={"distance": distance},
                )
                results[fit_id] = [{"x": p[0], "y": p[1]} for p in points]
            except Exception:
                results[fit_id] = []
        return results

    return await _exe(_compute)


@router.get("/ehp-speed")
async def ehp_vs_speed(fitIDs: str):
    """EHP vs speed graph."""
    fit_ids = _parse_ids(fitIDs)

    def _compute():
        from graphs.graph import FitGraph
        results = {}
        for fit_id in fit_ids:
            try:
                graph = FitGraph.getInstance()
                points = graph.getPlotPoints(
                    fit_id,
                    "ehpSpeed",
                    xRange=(0, 5000),
                    xSteps=100,
                )
                results[fit_id] = [{"x": p[0], "y": p[1]} for p in points]
            except Exception:
                results[fit_id] = []
        return results

    return await _exe(_compute)
