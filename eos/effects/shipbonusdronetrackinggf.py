# shipBonusDroneTrackingGF
#
# Used by:
# Ships named like: Tristan (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF") * level)
