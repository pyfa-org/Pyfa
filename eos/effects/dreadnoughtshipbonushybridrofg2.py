# Used by:
# Ship: Moros
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusG2") * level)
