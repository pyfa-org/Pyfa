# Used by:
# Subsystem: Loki Electronics - Dissolution Sequencer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Electronic Systems").level
    fit.ship.boostItemAttr("scanLadarStrength", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic") * level)
