# subSystemBonusMinmatarDefensiveSkirmishWarfare
#
# Used by:
# Subsystem: Loki Defensive - Warfare Processor
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command Specialist"),
                                  "commandBonus", module.getModifiedItemAttr("subsystemBonusMinmatarDefensive"), skill="Minmatar Defensive Systems")
