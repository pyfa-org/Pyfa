# subSystemBonusMinmatarDefensiveSiegeWarfare
#
# Used by:
# Subsystem: Loki Defensive - Warfare Processor
type = "passive"


def handler(fit, src, context):
    attrs = ["warfareBuff1Value", "warfareBuff2Value", "warfareBuff3Value", "warfareBuff4Value", "buffDuration"]

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Command"), attrs,
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive"), skill="Minmatar Defensive Systems")
