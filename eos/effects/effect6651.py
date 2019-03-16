# shipModuleAncillaryRemoteArmorRepairer
#
# Used by:
# Modules from group: Ancillary Remote Armor Repairer (4 of 4)

type = "projected", "active"
runTime = "late"


def handler(fit, module, context, **kwargs):
    if "projected" not in context:
        return

    if module.charge and module.charge.name == "Nanite Repair Paste":
        multiplier = 3
    else:
        multiplier = 1

    amount = module.getModifiedItemAttr("armorDamageAmount") * multiplier
    speed = module.getModifiedItemAttr("duration") / 1000.0
    rps = amount / speed
    fit.extraAttributes.increase("armorRepair", rps)
    fit.extraAttributes.increase("armorRepairPreSpool", rps)
    fit.extraAttributes.increase("armorRepairFullSpool", rps)
