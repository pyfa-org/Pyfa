# missileSkillWarheadUpgradesThermalDamageBonus
#
# Used by:
# Implants named like: Agency 'Pyrolancea' DB Dose (4 of 4)
# Skill: Warhead Upgrades
type = "passive"


def handler(fit, src, context):
    mod = src.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "thermalDamage", src.getModifiedItemAttr("damageMultiplierBonus") * mod)
