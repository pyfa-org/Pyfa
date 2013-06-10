# Used by:
# Modules from group: Stasis Web (19 of 19)
# Modules from group: Warp Scrambler (38 of 39)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxRange", module.getModifiedItemAttr("overloadRangeBonus"),
                         stackingPenalties = True)