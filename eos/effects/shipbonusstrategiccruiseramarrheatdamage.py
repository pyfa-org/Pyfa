# Used by:
# Ship: Legion
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Strategic Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserAmarr") * level)
