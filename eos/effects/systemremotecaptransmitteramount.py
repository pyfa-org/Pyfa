# systemRemoteCapTransmitterAmount
#
# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, beacon, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                     "powerTransferAmount", beacon.getModifiedItemAttr("energyTransferAmountBonus"),
                                     stackingPenalties=True, penaltyGroup="postMul")
