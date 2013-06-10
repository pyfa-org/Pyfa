# Used by:
# Subsystem: Tengu Engineering - Power Core Multiplier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Engineering Systems").level
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusCaldariEngineering") * level)
