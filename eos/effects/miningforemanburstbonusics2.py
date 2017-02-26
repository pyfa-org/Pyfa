# miningForemanBurstBonusICS2
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
