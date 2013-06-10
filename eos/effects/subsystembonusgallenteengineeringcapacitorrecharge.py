# Used by:
# Subsystem: Proteus Engineering - Capacitor Regeneration Matrix
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Engineering Systems").level
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusGallenteEngineering") * level)
