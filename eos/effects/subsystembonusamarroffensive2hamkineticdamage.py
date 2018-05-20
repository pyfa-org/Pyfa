# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "kineticDamage", module.getModifiedItemAttr("subsystemBonusAmarrOffensive2"),
                                    skill="Amarr Offensive Systems")
