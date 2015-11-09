# overloadSelfThermalHardeningBonus
#
# Used by:
# Variations of module: Armor Thermal Hardener I (39 of 39)
# Variations of module: Thermal Dissipation Field I (19 of 19)
# Module: Civilian Thermal Dissipation Field
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("thermalDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))