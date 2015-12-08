# systemEnergyNeutMultiplier
#
# Used by:
# Celestials named like: Pulsar Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")
def handler(fit, beacon, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                     "energyDestabilizationAmount", beacon.getModifiedItemAttr("energyWarfareStrengthMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
