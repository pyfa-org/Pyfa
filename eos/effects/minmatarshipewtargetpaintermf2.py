# minmatarShipEwTargetPainterMF2
#
# Used by:
# Ship: Hyena
# Ship: Vigil
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
