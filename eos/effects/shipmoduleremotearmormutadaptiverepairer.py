# ShipModuleRemoteArmorMutadaptiveRepairer
#
# Used by:
# Modules from group: Mutadaptive Remote Armor Repairer (5 of 5)
from eos.utils.spoolSupport import SpoolType, calculateSpoolup


type = "projected", "active"


def handler(fit, container, context, **kwargs):
    if "projected" in context:
        repAmountBase = container.getModifiedItemAttr("armorDamageAmount")
        cycleTime = container.getModifiedItemAttr("duration") / 1000.0
        repSpoolMax = container.getModifiedItemAttr("repairMultiplierBonusMax")
        repSpoolPerCycle = container.getModifiedItemAttr("repairMultiplierBonusPerCycle")
        repAmount = repAmountBase * (1 + calculateSpoolup(repSpoolMax, repSpoolPerCycle, cycleTime, container.spoolType, container.spoolAmount))
        fit.extraAttributes.increase("armorRepair", repAmount / cycleTime, **kwargs)
