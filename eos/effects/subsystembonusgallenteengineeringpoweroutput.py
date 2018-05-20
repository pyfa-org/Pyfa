# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("powerOutput", module.getModifiedItemAttr("subsystemBonusGallenteCore"),
                           skill="Gallente Core Systems")
