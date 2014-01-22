# Used by:
# Subsystem: Legion Propulsion - Interdiction Nullifier
# Subsystem: Loki Propulsion - Interdiction Nullifier
# Subsystem: Proteus Propulsion - Interdiction Nullifier
# Subsystem: Tengu Propulsion - Interdiction Nullifier
type = "passive"
def handler(fit, module, context):
    fit.ship.forceItemAttr("warpBubbleImmune", module.getModifiedItemAttr("warpBubbleImmuneModifier"))
