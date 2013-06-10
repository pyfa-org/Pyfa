# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    fit.ship.boostItemAttr("shieldKineticDamageResonance", beacon.getModifiedItemAttr("shieldKineticDamageResistanceBonus"),
                           stackingPenalties = True)
