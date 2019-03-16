# shipBonusRemoteArmorRepairCapNeedAC1
#
# Used by:
# Ship: Augoror
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
