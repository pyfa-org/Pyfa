# Used by:
# Implants named like: Electronics Upgrades (6 of 6)
# Modules named like: Liquid (8 of 8)
# Skill: Electronics Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Electronics Upgrades"),
                                  "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)
