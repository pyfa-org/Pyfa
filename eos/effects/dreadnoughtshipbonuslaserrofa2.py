# Used by:
# Ship: Revelation
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusA2") * level)
