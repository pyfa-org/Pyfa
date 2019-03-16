# fueledShieldBoosting
#
# Used by:
# Modules from group: Ancillary Shield Booster (8 of 8)
runTime = "late"
type = "active"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
