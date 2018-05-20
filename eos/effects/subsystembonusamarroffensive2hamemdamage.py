# subsystemBonusAmarrOffensive2HAMEmDamage
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "emDamage", module.getModifiedItemAttr("subsystemBonusAmarrOffensive2"),
                                    skill="Amarr Offensive Systems")
