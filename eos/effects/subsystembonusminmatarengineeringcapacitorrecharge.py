# subsystemBonusMinmatarEngineeringCapacitorRecharge
#
# Used by:
# Subsystem: Loki Engineering - Capacitor Regeneration Matrix
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering"), skill="Minmatar Engineering Systems")
