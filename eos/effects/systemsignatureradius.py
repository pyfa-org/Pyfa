# systemSignatureRadius
#
# Used by:
# Celestials named like: Pulsar Effect Beacon Class (6 of 6)
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, beacon, context):
    fit.ship.multiplyItemAttr("signatureRadius", beacon.getModifiedItemAttr("signatureRadiusMultiplier"),
                              stackingPenalties=True, penaltyGroup="postMul")
