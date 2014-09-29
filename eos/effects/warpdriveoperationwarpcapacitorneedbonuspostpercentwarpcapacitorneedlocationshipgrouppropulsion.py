# warpDriveOperationWarpCapacitorNeedBonusPostPercentWarpCapacitorNeedLocationShipGroupPropulsion
#
# Used by:
# Modules named like: Warp Core Optimizer (8 of 8)
# Skill: Warp Drive Operation
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr("warpCapacitorNeed", container.getModifiedItemAttr("warpCapacitorNeedBonus") * level,
                           stackingPenalties = "skill" not in context)
