# subsystemBonusCaldariOffensive3HMLHAMVelocity
#
# Used by:
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles") or mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", src.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                    skill="Caldari Offensive Systems")
