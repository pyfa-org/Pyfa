# Used by:
# Modules from group: Stasis Web (19 of 19)
# Variations of module: Warp Disruptor I (19 of 19)
# Variations of module: Warp Scrambler I (19 of 19)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxRange", module.getModifiedItemAttr("overloadRangeBonus"),
                         stackingPenalties = True)