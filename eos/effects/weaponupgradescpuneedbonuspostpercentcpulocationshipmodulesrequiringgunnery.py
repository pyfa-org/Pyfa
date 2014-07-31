# Used by:
# Implants named like: Zainou 'Gnome' Weapon Upgrades WU (6 of 6)
# Skill: Weapon Upgrades
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "cpu", container.getModifiedItemAttr("cpuNeedBonus") * level)
