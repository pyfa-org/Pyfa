# Used by:
# Modules from group: Armor Repair Unit (100 of 100)
runTime = "late"
type = "active"
def handler(fit, module, context):
    amount = module.getModifiedItemAttr("armorDamageAmount")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("armorRepair", amount / speed)