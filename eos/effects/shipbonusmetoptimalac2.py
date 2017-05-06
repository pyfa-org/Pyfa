# shipBonusMETOptimalAC2
#
# Used by:
# Ship: Enforcer
# Ship: Omen Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
