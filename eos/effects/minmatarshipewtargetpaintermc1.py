# minmatarShipEwTargetPainterMC1
#
# Used by:
# Ship: Bellicose
# Ship: Rapier
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Target Painter",
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMC") * level)
