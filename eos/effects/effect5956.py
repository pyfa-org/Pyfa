# shipMETDamageBonusAC2
#
# Used by:
# Ship: Devoter
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
