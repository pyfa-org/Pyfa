# Used by:
# Subsystem: Tengu Electronics - Dissolution Sequencer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Electronic Systems").level
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("subsystemBonusCaldariElectronic2") * level)
