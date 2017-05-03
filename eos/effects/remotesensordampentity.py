# remoteSensorDampEntity
#
# Used by:
# Drones named like: SD (3 of 3)
type = "projected", "active"


def handler(fit, module, context, *args, **kwargs):
    if "projected" not in context:
        return

    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                           stackingPenalties=True, *args, **kwargs)

    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties=True, *args, **kwargs)
