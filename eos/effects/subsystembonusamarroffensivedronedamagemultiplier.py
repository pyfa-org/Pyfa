# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", module.getModifiedItemAttr("subsystemBonusAmarrOffensive"),
                                 skill="Amarr Offensive Systems")
