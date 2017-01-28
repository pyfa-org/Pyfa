# eliteBonusLogisticRemoteArmorRepairDuration3
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "duration",
                                  src.getModifiedItemAttr("eliteBonusLogistics3"), skill="Logistics Cruisers")
