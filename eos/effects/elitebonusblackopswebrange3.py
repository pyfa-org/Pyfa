# eliteBonusBlackOpsWebRange3
#
# Used by:
# Ship: Marshal
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange",
                                  src.getModifiedItemAttr("eliteBonusBlackOps3"), stackingPenalties=True, skill="Black Ops")
