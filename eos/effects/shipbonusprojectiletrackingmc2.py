# shipBonusProjectileTrackingMC2
#
# Used by:
# Ship: Stabber Fleet Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
