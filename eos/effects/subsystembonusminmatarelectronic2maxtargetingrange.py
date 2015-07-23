# subsystemBonusMinmatarElectronic2MaxTargetingRange
#
# Used by:
# Subsystem: Loki Electronics - Dissolution Sequencer
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic2"), skill="Minmatar Electronic Systems")
