# subSystemBonusCaldariDefensiveSkirmishWarfare
#
# Used by:
# Subsystem: Tengu Defensive - Warfare Processor
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"), attrs,
                                  src.getModifiedItemAttr("subsystemBonusCaldariDefensive"), skill="Caldari Defensive Systems")
