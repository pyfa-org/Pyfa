# shipBonusMWDSignatureRadiusMD2
#
# Used by:
# Ship: Talwar
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMD2"),
                                  skill="Minmatar Destroyer")
