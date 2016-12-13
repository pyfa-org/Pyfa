type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Defender Missiles"),
                                  "moduleReactivationDelay", ship.getModifiedItemAttr("shipBonusRole1"))
