# miningForemanBurstBonusORECapital2
#
# Used by:
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                  src.getModifiedItemAttr("shipBonusORECapital2"), skill="Capital Industrial Ships")
