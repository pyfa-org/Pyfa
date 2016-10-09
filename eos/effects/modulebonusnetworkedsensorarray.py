# moduleBonusNetworkedSensorArray
#
# Used by:
# Module: Networked Sensor Array
type = "active"
def handler(fit, src, context):
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("scanResolutionBonus"), stackingPenalties=True)

    for scanType in ('Magnetometric', 'Ladar', 'Gravimetric', 'Radar'):
        attr = "scan{}Strength".format(scanType)
        bonus = src.getModifiedItemAttr("scan{}StrengthPercent".format(scanType))
        fit.ship.boostItemAttr(attr, bonus, stackingPenalties=True)
        fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), attr, bonus, stackingPenalties=True)

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