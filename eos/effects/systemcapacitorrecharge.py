# systemCapacitorRecharge
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
# Celestials named like: Pulsar Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("rechargeRate", beacon.getModifiedItemAttr("rechargeRateMultiplier"))
