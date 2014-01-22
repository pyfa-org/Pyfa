# Used by:
# Implants named like: Warp WS (6 of 6)
# Modules named like: Velocity Optimizer (8 of 8)
# Implant: Ascendancy Alpha
# Implant: Ascendancy Beta
# Implant: Ascendancy Delta
# Implant: Ascendancy Epsilon
# Implant: Ascendancy Gamma
# Implant: Low-grade Ascendancy Alpha
# Implant: Low-grade Ascendancy Beta
# Implant: Low-grade Ascendancy Delta
# Implant: Low-grade Ascendancy Epsilon
# Implant: Low-grade Ascendancy Gamma
type = "passive"
def handler(fit, container, context):
    fit.ship.boostItemAttr("baseWarpSpeed", container.getModifiedItemAttr("WarpSBonus"))
