# capitalLauncherSkillCruiseCitadelKineticDamage1
#
# Used by:
# Skill: XL Cruise Missiles
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Cruise Missiles"),
                                    "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
