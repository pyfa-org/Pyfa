# warpSkillSpeed
#
# Used by:
# Implants named like: Eifyr and Co. 'Rogue' Warp Drive Speed WS (6 of 6)
# Implants named like: grade Ascendancy (10 of 12)
# Modules named like: Hyperspatial Velocity Optimizer (8 of 8)
type = "passive"
def handler(fit, container, context):
    penalized = False if "skill" in context or "implant" in context else True
    fit.ship.boostItemAttr("baseWarpSpeed", container.getModifiedItemAttr("WarpSBonus"),
                           stackingPenalties=penalized)
