# shipModuleTrackingDisruptor
#
# Used by:
# Variations of module: Tracking Disruptor I (6 of 6)
type = "projected", "active"


def handler(fit, module, context, *args, **kwargs):
    if "projected" in context:
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True, *args, **kwargs)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True, *args, **kwargs)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True, *args, **kwargs)
