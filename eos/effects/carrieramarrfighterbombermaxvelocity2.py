# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Carrier").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighter Bombers"),
                                 "maxVelocity", ship.getModifiedItemAttr("carrierAmarrBonus2") * level)
