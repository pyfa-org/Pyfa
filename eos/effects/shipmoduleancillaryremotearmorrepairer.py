# shipModuleAncillaryRemoteArmorRepairer
#
# Used by:
# Modules from group: Ancillary Remote Armor Repairer (4 of 4)
runTime = "late"
type = "projected", "active"


def handler(fit, module, context, **kwargs):
    if "projected" not in context:
        return

    if module.charge and module.charge.name == "Nanite Repair Paste":
        multiplier = 3
    else:
        multiplier = 1

    amount = module.getModifiedItemAttr("armorDamageAmount") * multiplier
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("armorRepair", amount / speed, **kwargs)
