# miningForemanBurstBonusICS2
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff4Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff1Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "buffDuration",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff3Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), "warfareBuff2Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS2"), skill="Industrial Command Ships")
