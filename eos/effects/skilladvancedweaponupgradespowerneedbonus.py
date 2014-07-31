# Used by:
# Skill: Advanced Weapon Upgrades
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery") or mod.item.requiresSkill("Missile Launcher Operation"),
                                  "power", skill.getModifiedItemAttr("powerNeedBonus") * skill.level)
