# Used by:
# Modules from group: Remote Hull Repairer (7 of 7)
type = "projected", "active"
runTime = "late"
def handler(fit, module, context):
    if "projected" not in context: return
    bonus = module.getModifiedItemAttr("structureDamageAmount")
    duration = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("hullRepair", bonus / duration)
