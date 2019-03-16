# shipBonusRemoteArmorRepairAmountGC2
#
# Used by:
# Ship: Exequror
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "armorDamageAmount", src.getModifiedItemAttr("shipBonusGC2"),
                                  skill="Gallente Cruiser")
