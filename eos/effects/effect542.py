# shipCapNeedBonusAB
#
# Used by:
# Variations of ship: Armageddon (3 of 5)
# Ship: Apocalypse Imperial Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")
