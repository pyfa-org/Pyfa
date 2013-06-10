# Used by:
# Ship: Loki
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Strategic Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserMinmatar") * level)
