# Used by:
# Ships named like: Rokh (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCB") * level)
