# shipBonusDroneMiningAmountGC2
#
# Used by:
# Ships named like: Vexor (3 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", ship.getModifiedItemAttr("shipBonusGC2") * level)
