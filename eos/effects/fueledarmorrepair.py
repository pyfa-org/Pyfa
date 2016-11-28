# fueledArmorRepair
#
# Used by:
# Modules from group: Ancillary Armor Repairer (4 of 4)
runTime = "late"
type = "active"


def handler(fit, module, context):
    if module.charge:
        module.multiplyItemAttr("armorDamageAmount", module.getModifiedItemAttr("chargedArmorDamageMultiplier"))
        number_of_charges = module.getModifiedItemAttr("chargeRate") * (module.getModifiedItemAttr("capacity") /
                                                                        getattr(module.charge, "volume", False))
        reload_time = module.getModifiedItemAttr("reloadTime")
        if not reload_time:
            reload_time = 0
    else:
        number_of_charges = 0
        reload_time = 0

    if number_of_charges:
        amount = module.getModifiedItemAttr("armorDamageAmount") * number_of_charges
        speed = ((module.getModifiedItemAttr("duration") * number_of_charges) + reload_time) / 1000
    else:
        amount = module.getModifiedItemAttr("armorDamageAmount")
        speed = module.getModifiedItemAttr("duration") / 1000

    fit.extraAttributes.increase("armorRepair", amount / speed)
