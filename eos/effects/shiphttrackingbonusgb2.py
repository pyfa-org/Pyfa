# Used by:
# Ship: Megathron
# Ship: Megathron Federate Issue
# Ship: Megathron Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB2") * level)
