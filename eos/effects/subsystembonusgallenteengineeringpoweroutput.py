# Used by:
# Subsystem: Proteus Engineering - Power Core Multiplier
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Engineering Systems").level
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusGallenteEngineering") * level)
