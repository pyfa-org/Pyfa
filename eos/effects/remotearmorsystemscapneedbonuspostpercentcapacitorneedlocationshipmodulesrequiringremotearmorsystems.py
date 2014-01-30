# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Armor Implants > Implant Slot 07 (6 of 6)
# Variations of module: Large Remote Repair Augmentor I (2 of 2)
# Variations of module: Medium Remote Repair Augmentor I (2 of 2)
# Variations of module: Small Remote Repair Augmentor I (2 of 2)
# Skill: Remote Armor Repair Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
