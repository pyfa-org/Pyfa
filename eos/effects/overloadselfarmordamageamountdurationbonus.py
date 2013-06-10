# Used by:
# Modules from group: Armor Repair Unit (100 of 100)
# Modules from group: Fueled Armor Repairer (3 of 3)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus"))
    module.boostItemAttr("armorDamageAmount", module.getModifiedItemAttr("overloadArmorDamageAmount"))