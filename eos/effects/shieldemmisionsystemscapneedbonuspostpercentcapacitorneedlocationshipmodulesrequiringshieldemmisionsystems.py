# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Shield Implants > Implant Slot 08 (6 of 6)
# Skill: Shield Emission Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
