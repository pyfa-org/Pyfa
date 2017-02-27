# miningForemanStrengthBonus
#
# Used by:
# Skill: Mining Director
type = "passive"


def handler(fit, src, context):
    lvl = src.level

    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value"]
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Foreman"), attrs, src.getModifiedItemAttr("commandStrengthBonus") * lvl)

