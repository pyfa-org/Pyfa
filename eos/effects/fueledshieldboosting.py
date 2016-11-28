# fueledShieldBoosting
#
# Used by:
# Modules from group: Ancillary Shield Booster (5 of 5)
runTime = "late"
type = "active"


def handler(fit, module, context):
    if module.charge:
        number_of_charges = module.getModifiedItemAttr("chargeRate") * (module.getModifiedItemAttr("capacity") /
                                                                        getattr(module.charge, "volume", False))
        reload_time = module.getModifiedItemAttr("reloadTime")
        if not reload_time:
            reload_time = 0
    else:
        number_of_charges = 0
        reload_time = 0

    if number_of_charges:
        amount = module.getModifiedItemAttr("shieldBonus") * number_of_charges
        speed = ((module.getModifiedItemAttr("duration") * number_of_charges) + reload_time) / 1000
    else:
        amount = module.getModifiedItemAttr("shieldBonus")
        speed = module.getModifiedItemAttr("duration") / 1000

    fit.extraAttributes.increase("shieldRepair", amount / speed)
