# missileSkillRapidLauncherRoF
#
# Used by:
# Implants named like: Zainou 'Deadeye' Rapid Launch RL (6 of 6)
# Implant: Standard Cerebral Accelerator
# Implant: Whelan Machorin's Ballistic Smartlink
# Skill: Missile Launcher Operation
# Skill: Rapid Launch
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", container.getModifiedItemAttr("rofBonus") * level)
