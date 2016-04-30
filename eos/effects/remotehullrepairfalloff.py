# remoteHullRepairFalloff
#
# Used by:
# Modules from group: Remote Hull Repairer (8 of 8)
# Drones named like: Hull Maintenance Bot (6 of 6)
type = "projected", "active"
runTime = "late"
def handler(fit, module, context):
    if "projected" not in context: return
    bonus = module.getModifiedItemAttr("structureDamageAmount")
    duration = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("hullRepair", bonus / duration)
