# shipCruiseMissileVelocityBonusCB3
#
# Used by:
# Variations of ship: Raven (3 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3"), skill="Caldari Battleship")
