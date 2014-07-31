# Used by:
# Ships from group: Destroyer (9 of 18)
# Variations of ship: Catalyst (6 of 7)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))