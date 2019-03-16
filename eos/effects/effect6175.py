# battlecruiserMissileRange
#
# Used by:
# Ships named like: Drake (2 of 2)
# Ship: Cyclone
type = "passive"


def handler(fit, skill, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", skill.getModifiedItemAttr("roleBonusCBC"))
