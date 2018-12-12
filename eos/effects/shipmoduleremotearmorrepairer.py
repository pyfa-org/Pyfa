# shipModuleRemoteArmorRepairer
#
# Used by:
# Modules from group: Remote Armor Repairer (39 of 39)
type = "projected", "active"


def handler(fit, container, context, **kwargs):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.getModifiedItemAttr("duration") / 1000.0
        rps = bonus / duration
        fit.extraAttributes.increase("armorRepair", rps)
        fit.extraAttributes.increase("armorRepairPreSpool", rps)
        fit.extraAttributes.increase("armorRepairFullSpool", rps)
