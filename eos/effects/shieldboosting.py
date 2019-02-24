# shieldBoosting
#
# Used by:
# Modules from group: Shield Booster (97 of 97)
runTime = "late"
type = "active"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)
