# Used by:
# Implants named like: 'Squire' Upgrades EU (6 of 6)
# Modules named like: Powergrid Subroutine (8 of 8)
# Skill: Energy Grid Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Energy Grid Upgrades"),
                                  "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)
