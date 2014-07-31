# Used by:
# Ship: Vindicator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "speedFactor", ship.getModifiedItemAttr("shipBonusMB") * level)
