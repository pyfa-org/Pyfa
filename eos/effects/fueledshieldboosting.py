# Used by:
# Modules from group: Fueled Shield Booster (4 of 4)
runTime = "late"
type = "active"
def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
