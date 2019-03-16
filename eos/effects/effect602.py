# shipPTurretSpeedBonusMC
#
# Used by:
# Variations of ship: Rupture (3 of 3)
# Variations of ship: Stabber (3 of 3)
# Ship: Enforcer
# Ship: Huginn
# Ship: Scythe Fleet Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
