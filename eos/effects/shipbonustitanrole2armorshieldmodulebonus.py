# shipBonusTitanRole2ArmorShieldModuleBonus
#
# Used by:
# Ships from group: Titan (4 of 4)
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"), "armorHPBonusAdd", src.getModifiedItemAttr("shipBonusRole2"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Upgrades"), "capacityBonus", src.getModifiedItemAttr("shipBonusRole2"))
