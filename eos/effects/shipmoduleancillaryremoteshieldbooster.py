# shipModuleAncillaryRemoteShieldBooster
#
# Used by:
# Modules from group: Ancillary Remote Shield Booster (4 of 4)
runTime = "late"
type = "projected", "active"


def handler(fit, module, context, **kwargs):
    if "projected" not in context:
        return
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed, **kwargs)
