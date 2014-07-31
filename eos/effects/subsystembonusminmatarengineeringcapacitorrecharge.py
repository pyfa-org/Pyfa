# Used by:
# Subsystem: Loki Engineering - Capacitor Regeneration Matrix
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Engineering Systems").level
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering") * level)
