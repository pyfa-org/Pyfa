# eliteIndustrialFleetCapacity1
#
# Used by:
# Ships from group: Deep Space Transport (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("fleetHangarCapacity", ship.getModifiedItemAttr("eliteBonusIndustrial1"), skill="Transport Ships")
