# Used by:
# Modules from group: Fueled Armor Repairer (3 of 3)
runTime = "late"
type = "active"
def handler(fit, module, context):
    if module.charge and module.charge.name == "Nanite Repair Paste":
        module.multiplyItemAttr("armorDamageAmount", 3)
        
    amount = module.getModifiedItemAttr("armorDamageAmount")
    speed = module.getModifiedItemAttr("duration") / 1000.0
    fit.extraAttributes.increase("armorRepair", amount / speed)
