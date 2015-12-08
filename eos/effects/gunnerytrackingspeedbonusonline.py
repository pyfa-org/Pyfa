# gunneryTrackingSpeedBonusOnline
#
# Used by:
# Modules from group: Tracking Enhancer (17 of 17)
# Module: QA Damage Module
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                  stackingPenalties = True)