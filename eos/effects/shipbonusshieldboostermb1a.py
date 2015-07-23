# shipBonusShieldBoosterMB1a
#
# Used by:
# Ship: Maelstrom
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Booster",
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
