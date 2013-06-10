# Used by:
# Subsystem: Loki Engineering - Augmented Capacitor Reservoir
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Engineering Systems").level
    fit.ship.boostItemAttr("capacitorCapacity", module.getModifiedItemAttr("subsystemBonusMinmatarEngineering") * level)
