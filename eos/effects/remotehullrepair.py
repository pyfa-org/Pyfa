# Not used by any item
type = "projected", "active"
runTime = "late"


def handler(fit, module, context):
    if "projected" not in context:
        return
    bonus = module.getModifiedItemAttr("structureDamageAmount")
    duration = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("hullRepair", bonus / duration)
