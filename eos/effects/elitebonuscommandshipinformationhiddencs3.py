# Used by:
# Ships from group: Command Ship (4 of 8)
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonusHidden", module.getModifiedItemAttr("eliteBonusCommandShips3") * level)
