# subsystemBonusCaldariOffensive2MissileLauncherKineticDamage
#
# Used by:
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                    skill="Caldari Offensive Systems")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                    skill="Caldari Offensive Systems")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "kineticDamage", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                    skill="Caldari Offensive Systems")
