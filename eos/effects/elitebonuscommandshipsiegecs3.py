# Used by:
# Ship: Claymore
# Ship: Nighthawk
# Ship: Sleipnir
# Ship: Vulture
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"),
                                  "commandBonus", ship.getModifiedItemAttr("eliteBonusCommandShips3") * level)
