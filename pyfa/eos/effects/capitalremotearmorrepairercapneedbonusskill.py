# capitalRemoteArmorRepairerCapNeedBonusSkill
#
# Used by:
# Variations of module: Capital Remote Repair Augmentor I (2 of 2)
# Skill: Capital Remote Armor Repair Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Remote Armor Repair Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
