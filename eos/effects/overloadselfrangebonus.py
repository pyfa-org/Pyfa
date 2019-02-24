# overloadSelfRangeBonus
#
# Used by:
# Modules from group: Stasis Grappler (7 of 7)
# Modules from group: Stasis Web (19 of 19)
# Modules from group: Warp Scrambler (54 of 55)
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("maxRange", module.getModifiedItemAttr("overloadRangeBonus"),
                         stackingPenalties=True)
