# eliteBonusBlackOpsScramblerRange4
#
# Used by:
# Ship: Marshal
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler", "maxRange",
                                  src.getModifiedItemAttr("eliteBonusBlackOps4"), stackingPenalties=True, skill="Black Ops")
