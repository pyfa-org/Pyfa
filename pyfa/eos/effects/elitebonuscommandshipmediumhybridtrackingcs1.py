# eliteBonusCommandShipMediumHybridTrackingCS1
#
# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips1") * level)
