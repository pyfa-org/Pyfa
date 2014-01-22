# Used by:
# Ship: Apocalypse Imperial Issue
# Ship: Armageddon Imperial Issue
# Ship: Armageddon Navy Issue
# Ship: Redeemer
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAB") * level)
