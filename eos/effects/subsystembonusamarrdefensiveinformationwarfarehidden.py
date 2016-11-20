# subSystemBonusAmarrDefensiveInformationWarfareHidden
#
# Used by:
# Subsystem: Legion Defensive - Warfare Processor
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonusHidden", module.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
