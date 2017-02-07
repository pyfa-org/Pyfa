# eliteBonusLogisticRemoteArmorRepairOptimalFalloff1
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusLogistics1"),
                                  skill="Logistics Cruisers")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "maxRange",
                                  src.getModifiedItemAttr("eliteBonusLogistics1"),
                                  skill="Logistics Cruisers")
