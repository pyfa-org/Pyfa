# carrierGallenteDroneOwnDmg2
#
# Used by:
# Ship: Nyx
# Ship: Thanatos
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters"),
                                 "damageMultiplier", ship.getModifiedItemAttr("carrierGallenteBonus2"),
                                 skill="Gallente Carrier")
