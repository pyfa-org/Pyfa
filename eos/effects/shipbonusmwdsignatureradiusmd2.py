# Used by:
# Ship: Talwar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("shipBonusMD2") * level)
