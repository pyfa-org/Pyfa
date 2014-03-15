# Used by:
# Implants named like: Ascendancy (10 of 12)
# Implants named like: Eifyr and Co. 'Rogue' Warp Drive Speed WS (6 of 6)
# Modules named like: Hyperspatial Velocity Optimizer (8 of 8)
type = "passive"
def handler(fit, container, context):
    fit.ship.boostItemAttr("baseWarpSpeed", container.getModifiedItemAttr("WarpSBonus"))
