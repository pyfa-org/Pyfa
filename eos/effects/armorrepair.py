# armorRepair
#
# Used by:
# Modules from group: Armor Repair Unit (108 of 108)
runTime = "late"
type = "active"


def handler(fit, module, context):
    amount = module.getModifiedItemAttr("armorDamageAmount")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    rps = amount / speed
    fit.extraAttributes.increase("armorRepair", rps)
    fit.extraAttributes.increase("armorRepairPreSpool", rps)
    fit.extraAttributes.increase("armorRepairFullSpool", rps)
