# Used by:
# Subsystem: Legion Offensive - Covert Reconfiguration
# Subsystem: Loki Offensive - Covert Reconfiguration
# Subsystem: Proteus Offensive - Covert Reconfiguration
# Subsystem: Tengu Offensive - Covert Reconfiguration
type = "passive"
def handler(fit, module, context):
    fit.ship.forceItemAttr("jumpHarmonics", module.getModifiedItemAttr("jumpHarmonicsModifier"))
