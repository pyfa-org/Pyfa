# subsystemBonusAmarrElectronic2MaxTargetingRange
#
# Used by:
# Subsystem: Legion Electronics - Dissolution Sequencer
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("subsystemBonusAmarrElectronic2"), skill="Amarr Electronic Systems")
