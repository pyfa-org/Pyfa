# miningForemanMindLinkMiningAmountBonusReplacer
#
# Used by:
# Implant: Mining Foreman Mindlink
type = "gang"
gangBoost = "miningAmount"
gangBonus = "miningAmountBonus"
def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  gangBoost, container.getModifiedItemAttr(gangBonus))
