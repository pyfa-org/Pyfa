# Used by:
# Ship: Proteus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Strategic Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserGallente") * level)
