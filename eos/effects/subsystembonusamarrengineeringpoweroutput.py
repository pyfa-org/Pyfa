# Used by:
# Subsystem: Legion Engineering - Power Core Multiplier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Engineering Systems").level
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusAmarrEngineering") * level)
