# Used by:
# Skill: Warhead Upgrades
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosiveDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)