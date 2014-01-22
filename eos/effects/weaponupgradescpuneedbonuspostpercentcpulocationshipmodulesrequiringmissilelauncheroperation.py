# Used by:
# Implants named like: Launcher CPU LE (6 of 6)
# Skill: Weapon Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)
