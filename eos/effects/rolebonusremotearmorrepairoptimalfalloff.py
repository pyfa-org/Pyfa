# roleBonusRemoteArmorRepairOptimalFalloff
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "falloffEffectiveness",
                                  src.getModifiedItemAttr("roleBonusRepairRange"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "maxRange",
                                  src.getModifiedItemAttr("roleBonusRepairRange"))
