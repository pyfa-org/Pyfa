# shipHybridOptimalGD1
#
# Used by:
# Ship: Eris
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
