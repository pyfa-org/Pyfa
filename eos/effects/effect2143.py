# minmatarShipEwTargetPainterMC2
#
# Used by:
# Ship: Huginn
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMC2"),
                                  skill="Minmatar Cruiser")
