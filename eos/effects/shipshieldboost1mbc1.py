# shipShieldBoost1MBC1
#
# Used by:
# Variations of ship: Cyclone (2 of 2)
# Ship: Sleipnir
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMBC1"),
                                  skill="Minmatar Battlecruiser")
