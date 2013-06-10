# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.ship.boostItemAttr("shieldEmDamageResonance", beacon.getModifiedItemAttr("shieldEmDamageResistanceBonus"),
                           stackingPenalties = True)
