# shipRemoteArmorFalloffAC2
#
# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "falloffEffectiveness", src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
