# missileSkillFoFAoeCloudSizeBonus
#
# Used by:
# Implants named like: Zainou 'Snapshot' Auto Targeting Explosion Radius FR (6 of 6)
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("FoF Missiles"),
                                    "aoeCloudSize", container.getModifiedItemAttr("aoeCloudSizeBonus") * level)
