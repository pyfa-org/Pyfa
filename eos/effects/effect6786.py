# shieldCommandBurstBonusICS3
#
# Used by:
# Ship: Orca
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Multiplier",
                                  src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration",
                                  src.getModifiedItemAttr("shipBonusICS3"), skill="Industrial Command Ships")
