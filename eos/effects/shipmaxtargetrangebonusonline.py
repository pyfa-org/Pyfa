# shipMaxTargetRangeBonusOnline
#
# Used by:
# Modules from group: Signal Amplifier (7 of 7)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                           stackingPenalties = True)
