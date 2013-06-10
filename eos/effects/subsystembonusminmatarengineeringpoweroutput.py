# Used by:
# Subsystem: Loki Engineering - Power Core Multiplier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Engineering Systems").level
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering") * level)
