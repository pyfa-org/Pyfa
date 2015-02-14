# shipBonusDreadCitadelCruiseRofC1
#
# Used by:
# Ships named like: Phoenix (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Citadel Cruise Missiles"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusC1") * level)
