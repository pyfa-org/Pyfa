# Used by:
# Variations of module: Armor Kinetic Hardener I (39 of 39)
# Variations of module: Kinetic Deflection Field I (19 of 19)
# Module: Civilian Kinetic Deflection Field
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("kineticDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))