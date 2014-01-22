# Used by:
# Celestials named like: Black Hole Effect Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, beacon, context):
    amount = beacon.getModifiedItemAttr("droneRangeMultiplier")
    fit.extraAttributes.multiply("droneControlRange", amount)
