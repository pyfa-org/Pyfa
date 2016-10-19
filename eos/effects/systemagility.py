# systemAgility
#
# Used by:
# Celestials named like: Black Hole Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("agility", beacon.getModifiedItemAttr("agilityMultiplier"), stackingPenalties=True)
