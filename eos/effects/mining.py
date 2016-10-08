# miningDroneOperationMiningAmountBonusPostPercentMiningDroneAmountPercentChar
#
# Used by:
# Mining Drones

type = "passive"
def handler(fit, container, context):
    miningDroneAmountPercent = container.getModifiedItemAttr("miningDroneAmountPercent")
    if (miningDroneAmountPercent is None) or (miningDroneAmountPercent == 0):
        miningDroneAmountPercent = 1
    else:
        miningDroneAmountPercent = miningDroneAmountPercent/100

    fit.drones.filteredItemMultiply(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", miningDroneAmountPercent)
