# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"),
                                  skill="Amarr Propulsion Systems")
