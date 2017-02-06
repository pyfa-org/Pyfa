# capitalLauncherSkillCitadelThermalDamage
#
# Used by:
# Implants named like: Hardwiring Zainou 'Sharpshooter' ZMX (6 of 6)
# Skill: XL Torpedoes
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("XL Torpedoes"),
                                    "thermalDamage", container.getModifiedItemAttr("damageMultiplierBonus") * level)
