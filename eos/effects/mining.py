# miningDroneOperationMiningAmountBonusPostPercentMiningDroneAmountPercentChar
#
# Used by:
# Mining Drones

type = "passive"
grouped = True


def handler(fit, container, context):
    miningDroneAmountPercent = container.getModifiedItemAttr("miningDroneAmountPercent")
    if (miningDroneAmountPercent is None) or (miningDroneAmountPercent == 0):
        pass
    else:
        container.multiplyItemAttr("miningAmount", miningDroneAmountPercent / 100)
