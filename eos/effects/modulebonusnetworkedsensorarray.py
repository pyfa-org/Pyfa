# moduleBonusNetworkedSensorArray
#
# Used by:
# Module: Networked Sensor Array
type = "active"
def handler(fit, src, context):
    fit.ship.multiplyItemAttr("maxTargetRange", src.getModifiedItemAttr("maxTargetRangeMultiplier"), stackingPenalties=True, penaltyGroup="postMul")
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionBonus"), stackingPenalties=True)

    for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
        fit.ship.boostItemAttr("scan{}Strength".format(scanType),
                               src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
                               stackingPenalties=True)

    # EW cap need increase
    groups = [
        'Burst Jammer',
        'Weapon Disruptor',
        'ECM',
        'Stasis Grappler',
        'Sensor Dampener',
        'Target Painter']

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups or
                                              mod.item.requiresSkill("Propulsion Jamming"),
                                  "capacitorNeed", src.getModifiedItemAttr("ewCapacitorNeedBonus"))