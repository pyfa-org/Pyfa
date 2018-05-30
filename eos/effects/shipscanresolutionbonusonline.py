# shipScanResolutionBonusOnline
#
# Used by:
# Modules from group: Signal Amplifier (7 of 7)
# Structure Modules from group: Structure Signal Amplifier (2 of 2)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties=True)
