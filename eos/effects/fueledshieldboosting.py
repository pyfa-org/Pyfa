# fueledShieldBoosting
#
# Used by:
# Modules from group: Ancillary Shield Booster (5 of 5)
runTime = "late"
type = "active"
def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
