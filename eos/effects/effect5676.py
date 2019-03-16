# shipBonusSmallMissileExplosionRadiusCD2
#
# Used by:
# Ship: Flycatcher
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(
        lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
        "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")
