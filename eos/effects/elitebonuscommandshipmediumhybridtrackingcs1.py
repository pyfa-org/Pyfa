# eliteBonusCommandShipMediumHybridTrackingCS1
#
# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")
