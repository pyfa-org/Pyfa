# Used by:
# Implant: Inherent Implants 'Highwall' Mining Upgrades MU-1001
# Implant: Inherent Implants 'Highwall' Mining Upgrades MU-1003
# Implant: Inherent Implants 'Highwall' Mining Upgrades MU-1005
# Skill: Mining Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Upgrades"),
                                  "cpuPenaltyPercent", container.getModifiedItemAttr("miningUpgradeCPUReductionBonus") * level)
