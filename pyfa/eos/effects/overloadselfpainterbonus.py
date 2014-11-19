# overloadSelfPainterBonus
#
# Used by:
# Modules from group: Target Painter (9 of 9)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("signatureRadiusBonus", module.getModifiedItemAttr("overloadPainterStrengthBonus") or 0)
