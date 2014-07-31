# Used by:
# Subsystem: Tengu Engineering - Capacitor Regeneration Matrix
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Engineering Systems").level
    fit.ship.boostItemAttr("rechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariEngineering") * level)
