# Used by:
# Skill: Weapon Upgrades
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"),
                                  "cpu", skill.getModifiedItemAttr("cpuNeedBonus") * skill.level)