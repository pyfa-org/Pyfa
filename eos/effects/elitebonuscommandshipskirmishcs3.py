# Used by:
# Ship: Astarte
# Ship: Claymore
# Ship: Eos
# Ship: Sleipnir
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"),
                                  "commandBonus", ship.getModifiedItemAttr("eliteBonusCommandShips3") * level)
