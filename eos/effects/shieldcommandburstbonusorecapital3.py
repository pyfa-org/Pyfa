# shieldCommandBurstBonusORECapital3
#
# Used by:
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                  src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                  src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                  src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                  src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                  src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
