# shipETspeedBonusAB2
#
# Used by:
# Variations of ship: Armageddon (3 of 5)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusAB2") * level)