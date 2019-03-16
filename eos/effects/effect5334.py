# shipHybridOptimal1CBC1
#
# Used by:
# Variations of ship: Ferox (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCBC1"), skill="Caldari Battlecruiser")
