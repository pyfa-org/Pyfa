# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Warfare Specialist"),
                                  "commandBonusHidden", ship.getModifiedItemAttr("eliteBonusCommandShips2") * level)
