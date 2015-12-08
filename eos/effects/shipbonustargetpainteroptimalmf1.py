# shipBonusTargetPainterOptimalMF1
#
# Used by:
# Ship: Hyena
# Ship: Vigil
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Target Painting"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
