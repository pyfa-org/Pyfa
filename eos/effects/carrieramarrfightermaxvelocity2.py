# carrierAmarrFighterMaxVelocity2
#
# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters"),
                                 "maxVelocity", ship.getModifiedItemAttr("carrierAmarrBonus2"), skill="Amarr Carrier")
