# shipTrackingBonusAB
#
# Used by:
# Ship: Nightmare
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")
