# carrierGallenteBomberDroneOwnDmg2
#
# Used by:
# Ship: Nyx
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighter Bombers"),
                                 "damageMultiplier", ship.getModifiedItemAttr("carrierGallenteBonus2"), skill="Gallente Carrier")
