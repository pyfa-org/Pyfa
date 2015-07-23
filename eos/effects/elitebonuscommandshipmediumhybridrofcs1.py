# eliteBonusCommandShipMediumHybridRoFCS1
#
# Used by:
# Ship: Astarte
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")
