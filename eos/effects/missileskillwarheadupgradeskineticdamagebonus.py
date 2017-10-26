# missileSkillWarheadUpgradesKineticDamageBonus
#
# Used by:
# Implants named like: Agency Damage Booster (3 of 3)
# Skill: Warhead Upgrades
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
