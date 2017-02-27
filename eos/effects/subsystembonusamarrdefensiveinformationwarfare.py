# subSystemBonusAmarrDefensiveInformationWarfare
#
# Used by:
# Subsystem: Legion Defensive - Warfare Processor
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), attrs,
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"), skill="Amarr Defensive Systems")
