# Used by:
# Ship: Phoenix
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Citadel",
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusC1") * level)
