# minmatarShipEwTargetPainterMF2
#
# Used by:
# Variations of ship: Vigil (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
