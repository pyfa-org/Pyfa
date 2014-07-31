# Used by:
# Variations of module: Armor EM Hardener I (39 of 39)
# Variations of module: EM Ward Field I (19 of 19)
# Module: Civilian EM Ward Field
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("emDamageResistanceBonus", module.getModifiedItemAttr("overloadHardeningBonus"))