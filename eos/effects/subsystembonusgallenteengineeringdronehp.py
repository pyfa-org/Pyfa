# Not used by any item
type = "passive"


def handler(fit, module, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), layer,
                                     module.getModifiedItemAttr("subsystemBonusGallenteCore"),
                                     skill="Gallente Core Systems")
