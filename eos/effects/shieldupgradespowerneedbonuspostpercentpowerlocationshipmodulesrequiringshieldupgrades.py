# Used by:
# Modules named like: Core Charge Economizer (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Shield Implants > Implant Slot 06 (6 of 6)
# Skill: Shield Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Upgrades"),
                                  "power", container.getModifiedItemAttr("powerNeedBonus") * level)
