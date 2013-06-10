# Used by:
# Ship: Tengu
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Strategic Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserCaldari") * level)
