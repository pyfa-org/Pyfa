# Used by:
# Subsystem: Legion Engineering - Capacitor Regeneration Matrix
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Engineering Systems").level
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusAmarrEngineering") * level)
