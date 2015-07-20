# subsystemBonusCaldariOffensive3HeavyAssaultMissileVelocity
#
# Used by:
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "maxVelocity", module.getModifiedItemAttr("subsystemBonusCaldariOffensive3"), skill="Caldari Offensive Systems")
