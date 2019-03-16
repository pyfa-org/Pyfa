# gunneryMaxRangeFalloffTrackingSpeedBonus
#
# Used by:
# Modules from group: Tracking Computer (11 of 11)
type = "active"


def handler(fit, module, context):
    for attr in ("maxRange", "falloff", "trackingSpeed"):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      attr, module.getModifiedItemAttr("%sBonus" % attr),
                                      stackingPenalties=True)
