# Used by:
# Modules named like: Nanobot (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Armor Implants > Implant Slot 06 (7 of 7)
# Skill: Repair Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "duration", container.getModifiedItemAttr("durationSkillBonus") * level)
