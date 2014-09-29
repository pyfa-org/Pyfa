# shipBonusTargetPainterOptimalMF1
#
# Used by:
# Variations of ship: Vigil (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF") * level)
