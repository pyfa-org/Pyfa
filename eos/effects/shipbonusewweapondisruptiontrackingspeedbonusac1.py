# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Disruptor",
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("shipBonusAC") * level)
