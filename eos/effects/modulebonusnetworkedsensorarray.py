type = "passive"
def handler(fit, src, context):
    fit.ship.increaseItemAttr("maxLockedTargets", src.getModifiedItemAttr("maxLockedTargetsBonus"))
    fit.ship.multiplyItemAttr("maxTargetRange", src.getModifiedItemAttr("maxTargetRangeMultiplier"), stackingPenalties=True, penaltyGroup="postMul")
    fit.ship.multiplyItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionMultiplier"), stackingPenalties=True)

    for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
        fit.ship.boostItemAttr("scan{}Strength".format(scanType),
                               src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                               stackingPenalties=True)

    # EW cap need increase
    groups = [
        'Burst Jammer',
        'Weapon Disruptor',
        'ECM',
        'Sensor Dampener',
        'Target Painter']

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                              mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))
