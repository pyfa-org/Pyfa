# shipBonusAoeVelocityRocketsCD2
#
# Used by:
# Ship: Corax
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")
