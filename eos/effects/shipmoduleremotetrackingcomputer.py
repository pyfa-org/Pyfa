# shipModuleRemoteTrackingComputer
#
# Used by:
# Modules from group: Remote Tracking Computer (8 of 8)
type = "projected", "active"


def handler(fit, module, context):
    if "projected" in context:
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                      stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                      "falloff", module.getModifiedItemAttr("falloffBonus"),
                                      stackingPenalties=True)
