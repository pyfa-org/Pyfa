# systemTargetPainterMultiplier
#
# Used by:
# Celestials named like: Magnetar Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")
def handler(fit, beacon, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Target Painting"),
                                     "signatureRadiusBonus", beacon.getModifiedItemAttr("targetPainterStrengthMultiplier"),
                                     stackingPenalties=True, penaltyGroup="postMul")
