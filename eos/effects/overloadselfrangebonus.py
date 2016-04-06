# overloadSelfRangeBonus
#
# Used by:
# Modules from group: Stasis Grappler (7 of 7)
# Modules from group: Stasis Web (18 of 18)
# Modules from group: Warp Scrambler (52 of 53)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxRange", module.getModifiedItemAttr("overloadRangeBonus"),
                         stackingPenalties = True)