runTime = "late"
type = "projected", "active"
def handler(fit, module, context):
    if "projected" not in context: return
    amount = module.getModifiedItemAttr("shieldBonus")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("shieldRepair", amount / speed)