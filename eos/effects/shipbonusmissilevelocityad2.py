# shipBonusMissileVelocityAD2
#
# Used by:
# Ship: Heretic
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
