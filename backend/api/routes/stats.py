"""
Stats routes — /fits/{fit_id}/stats/...

The /stats/full endpoint is the primary one the mobile app calls after every
fit change.  All stat categories are returned in one JSON payload to minimise
round-trips over the local loopback.
"""

import asyncio
from typing import Optional

import eos.db
from fastapi import APIRouter, HTTPException

from backend.api.models.stats import (
    CapStats,
    DpsStats,
    EhpBreakdown,
    FittingResources,
    FullStats,
    NavigationStats,
    PriceStats,
    ResistProfile,
    ResourceUsage,
    SensorStrength,
    TankStats,
    TargetingStats,
    ValidationResult,
)

router = APIRouter()


def _exe(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _get_fit_or_404(fit_id: int):
    fit = eos.db.getFit(fit_id)
    if fit is None:
        raise HTTPException(status_code=404, detail=f"Fit {fit_id} not found")
    return fit


def _attr(fit, attr_name: str, default: float = 0.0) -> float:
    """Safely get a calculated attribute from the fit's ship."""
    try:
        val = fit.ship.getModifiedItemAttr(attr_name)
        return float(val) if val is not None else default
    except Exception:
        return default


def _build_full_stats(fit_id: int, damage_pattern_id: Optional[int] = None) -> FullStats:
    """Compute all stat categories for a fit. Called in thread executor."""
    from service.fit import Fit as sFit

    fit = _get_fit_or_404(fit_id)
    svc = sFit.getInstance()

    # Recalculate (EOS is stateful; this ensures up-to-date numbers)
    svc.recalc(fit)

    # --- Validation ---
    issues = []
    try:
        validation_issues = svc.validateFit(fit_id)
        issues = [str(v) for v in validation_issues] if validation_issues else []
    except Exception:
        pass
    validation = ValidationResult(valid=(len(issues) == 0), issues=issues)

    # --- Tank ---
    def resist(layer_prefix):
        return ResistProfile(
            hp=_attr(fit, f"{layer_prefix}Hp"),
            em=_attr(fit, f"{layer_prefix}EmDamageResonance"),
            therm=_attr(fit, f"{layer_prefix}ThermalDamageResonance"),
            kin=_attr(fit, f"{layer_prefix}KineticDamageResonance"),
            exp=_attr(fit, f"{layer_prefix}ExplosiveDamageResonance"),
        )

    try:
        ehp_data = svc.getEHP(fit_id)
        ehp = EhpBreakdown(
            uniform=ehp_data.get("ehpUniform", 0.0),
            em=ehp_data.get("ehpEM", 0.0),
            therm=ehp_data.get("ehpTherm", 0.0),
            kin=ehp_data.get("ehpKin", 0.0),
            exp=ehp_data.get("ehpExp", 0.0),
        )
        effective_hp = ehp_data.get("ehpUniform", 0.0)
    except Exception:
        ehp = EhpBreakdown(uniform=0, em=0, therm=0, kin=0, exp=0)
        effective_hp = 0.0

    tank = TankStats(
        shield=resist("shield"),
        armor=resist("armor"),
        hull=resist("hull"),
        ehp=ehp,
        effectivehp=effective_hp,
    )

    # --- DPS ---
    try:
        dps_data = svc.getDPS(fit_id)
        dps = DpsStats(
            turret=float(dps_data.get("turret", 0)),
            missile=float(dps_data.get("missile", 0)),
            drone=float(dps_data.get("drone", 0)),
            total=float(dps_data.get("total", 0)),
            volley=float(dps_data.get("volley", 0)),
        )
    except Exception:
        dps = DpsStats(turret=0, missile=0, drone=0, total=0, volley=0)

    # --- Capacitor ---
    try:
        cap_data = svc.getCapacitorState(fit_id)
        cap = CapStats(
            stable=cap_data.get("stable", False),
            stableAt=cap_data.get("stableAt"),
            timeToEmpty=cap_data.get("timeToEmpty"),
            capacity=float(_attr(fit, "capacitorCapacity")),
            rechargeRate=float(_attr(fit, "rechargeRate")),
        )
    except Exception:
        cap = CapStats(stable=False, stableAt=None, timeToEmpty=None, capacity=0, rechargeRate=0)

    # --- Navigation ---
    nav = NavigationStats(
        maxVelocity=_attr(fit, "maxVelocity"),
        agility=_attr(fit, "agility"),
        alignTime=_attr(fit, "alignTime"),
        warpSpeed=_attr(fit, "warpSpeedMultiplier", 1.0) * 3.0,
        signatureRadius=_attr(fit, "signatureRadius"),
    )

    # --- Targeting ---
    sensor_type = "radar"
    sensor_value = 0.0
    for sensor in ("radar", "magnetometric", "gravimetric", "ladar"):
        val = _attr(fit, f"{sensor}Strength")
        if val > 0:
            sensor_type = sensor
            sensor_value = val
            break

    targeting = TargetingStats(
        maxTargetRange=_attr(fit, "maxTargetRange"),
        scanResolution=_attr(fit, "scanResolution"),
        maxLockedTargets=int(_attr(fit, "maxLockedTargets")),
        sensorStrength=SensorStrength(type=sensor_type, value=sensor_value),
    )

    # --- Fitting resources ---
    fitting = FittingResources(
        cpu=ResourceUsage(
            used=_attr(fit, "cpuLoad"),
            total=_attr(fit, "cpuOutput"),
        ),
        powergrid=ResourceUsage(
            used=_attr(fit, "powerLoad"),
            total=_attr(fit, "powerOutput"),
        ),
        calibration=ResourceUsage(
            used=_attr(fit, "upgradeCost"),
            total=_attr(fit, "upgradeCapacity"),
        ),
        droneBandwidth=ResourceUsage(
            used=_attr(fit, "droneBandwidthUsed"),
            total=_attr(fit, "droneBandwidth"),
        ),
        droneBay=ResourceUsage(
            used=_attr(fit, "droneCapacityUsed"),
            total=_attr(fit, "droneCapacity"),
        ),
    )

    # --- Price ---
    try:
        price_data = svc.getPrice(fit_id)
        price = PriceStats(
            hull=float(price_data.get("hull", 0)),
            fit=float(price_data.get("fit", 0)),
            total=float(price_data.get("total", 0)),
        )
    except Exception:
        price = PriceStats(hull=0, fit=0, total=0)

    return FullStats(
        fitID=fit_id,
        shipName=fit.ship.item.name,
        shipTypeID=fit.ship.item.typeID,
        validation=validation,
        tank=tank,
        dps=dps,
        capacitor=cap,
        navigation=nav,
        targeting=targeting,
        fitting=fitting,
        price=price,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/{fit_id}/stats/full", response_model=FullStats)
async def get_full_stats(fit_id: int, damagePattern: Optional[int] = None):
    """
    Primary stats endpoint — returns all stat categories in one call.
    The mobile app calls this after every fit modification.
    """
    return await _exe(_build_full_stats, fit_id, damagePattern)


@router.get("/{fit_id}/stats/ehp")
async def get_ehp(fit_id: int, damagePattern: Optional[int] = None):
    def _get():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        return sFit.getInstance().getEHP(fit_id)
    return await _exe(_get)


@router.get("/{fit_id}/stats/dps")
async def get_dps(
    fit_id: int,
    damagePattern: Optional[int] = None,
    targetProfile: Optional[int] = None,
):
    def _get():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        return sFit.getInstance().getDPS(fit_id)
    return await _exe(_get)


@router.get("/{fit_id}/stats/cap")
async def get_cap(fit_id: int):
    def _get():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        return sFit.getInstance().getCapacitorState(fit_id)
    return await _exe(_get)


@router.get("/{fit_id}/stats/navigation")
async def get_navigation(fit_id: int):
    def _get():
        fit = _get_fit_or_404(fit_id)
        return {
            "maxVelocity": _attr(fit, "maxVelocity"),
            "agility": _attr(fit, "agility"),
            "alignTime": _attr(fit, "alignTime"),
            "warpSpeed": _attr(fit, "warpSpeedMultiplier", 1.0) * 3.0,
            "signatureRadius": _attr(fit, "signatureRadius"),
        }
    return await _exe(_get)


@router.get("/{fit_id}/stats/targeting")
async def get_targeting(fit_id: int):
    def _get():
        fit = _get_fit_or_404(fit_id)
        return {
            "maxTargetRange": _attr(fit, "maxTargetRange"),
            "scanResolution": _attr(fit, "scanResolution"),
            "maxLockedTargets": int(_attr(fit, "maxLockedTargets")),
        }
    return await _exe(_get)


@router.get("/{fit_id}/validate")
async def validate_fit(fit_id: int):
    def _validate():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        issues = sFit.getInstance().validateFit(fit_id)
        return {"valid": not issues, "issues": [str(i) for i in (issues or [])]}
    return await _exe(_validate)
