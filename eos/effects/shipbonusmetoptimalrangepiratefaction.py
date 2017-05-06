# shipBonusMETOptimalRangePirateFaction
#
# Used by:
# Ships named like: Stratios (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusRole7"))
