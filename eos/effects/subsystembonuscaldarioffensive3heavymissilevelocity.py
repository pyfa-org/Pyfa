# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "maxVelocity", module.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                    skill="Caldari Offensive Systems")
