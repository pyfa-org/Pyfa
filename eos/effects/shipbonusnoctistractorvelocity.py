# shipBonusNoctisTractorVelocity
#
# Used by:
# Ship: Noctis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", ship.getModifiedItemAttr("shipBonusOreIndustrial2"),
                                  skill="ORE Industrial")
