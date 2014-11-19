# shipBonusMETOptimalAC2
#
# Used by:
# Ship: Omen Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAC2") * level)
