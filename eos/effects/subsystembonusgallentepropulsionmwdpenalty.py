# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus",
                                  module.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                                  skill="Gallente Propulsion Systems")
