# miningForemanBurstBonusICS2
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), attr,
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
