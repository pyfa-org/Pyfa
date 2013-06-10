# Used by:
# Implants named like: Inherent Implants 'Highwall' Mining Upgrades MU (3 of 3)
# Skill: Mining Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Upgrades"),
                                  "cpuPenaltyPercent", container.getModifiedItemAttr("miningUpgradeCPUReductionBonus") * level)
