# subsystemBonusCaldariEngineeringCapacitorRecharge
#
# Used by:
# Subsystem: Tengu Engineering - Capacitor Regeneration Matrix
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariEngineering"),
                           skill="Caldari Engineering Systems")
