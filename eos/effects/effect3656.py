# gunneryTrackingSpeedBonusOnline
#
# Used by:
# Modules from group: Tracking Enhancer (10 of 10)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                  stackingPenalties=True)
