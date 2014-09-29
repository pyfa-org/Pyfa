# shipBonusShieldBoosterMB1a
#
# Used by:
# Ships named like: Maelstrom (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Booster",
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMB") * level)
