# subSystemBonusCaldariDefensiveInformationWarfare
#
# Used by:
# Subsystem: Tengu Defensive - Warfare Processor
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonus", module.getModifiedItemAttr("subsystemBonusCaldariDefensive"), skill="Caldari Defensive Systems")
