# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), "maxVelocity",
                                 module.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                                 skill="Gallente Core Systems")
