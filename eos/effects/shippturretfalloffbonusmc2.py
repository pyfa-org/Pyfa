# shipPTurretFalloffBonusMC2
#
# Used by:
# Ship: Enforcer
# Ship: Stabber
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
