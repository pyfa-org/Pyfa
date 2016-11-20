# shieldCommandBurstBonusORECapital3
#
# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff4Modifier", src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "buffDuration", src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff1Modifier", src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff3Modifier", src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), "warfareBuff2Modifier", src.getModifiedItemAttr("shipBonusORECapital3"), skill="Capital Industrial Ships")
