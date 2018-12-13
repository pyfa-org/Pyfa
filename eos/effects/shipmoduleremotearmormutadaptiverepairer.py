# ShipModuleRemoteArmorMutadaptiveRepairer
#
# Used by:
# Modules from group: Mutadaptive Remote Armor Repairer (5 of 5)


from eos.utils.spoolSupport import SpoolType, SpoolOptions, calculateSpoolup, resolveSpoolOptions


type = "projected", "active"


def handler(fit, container, context, **kwargs):
    if "projected" in context:
        repAmountBase = container.getModifiedItemAttr("armorDamageAmount")
        cycleTime = container.getModifiedItemAttr("duration") / 1000.0
        repSpoolMax = container.getModifiedItemAttr("repairMultiplierBonusMax")
        repSpoolPerCycle = container.getModifiedItemAttr("repairMultiplierBonusPerCycle")
        # TODO: fetch spoolup option
        defaultSpoolValue = 1
        spoolType, spoolAmount = resolveSpoolOptions(
            SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False),
            container)
        rps = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, spoolType, spoolAmount)[0]) / cycleTime
        rpsPreSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 0)[0]) / cycleTime
        rpsFullSpool = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, SpoolType.SCALE, 1)[0]) / cycleTime
        fit.extraAttributes.increase("armorRepair", rps, **kwargs)
        fit.extraAttributes.increase("armorRepairPreSpool", rpsPreSpool, **kwargs)
        fit.extraAttributes.increase("armorRepairFullSpool", rpsFullSpool, **kwargs)
