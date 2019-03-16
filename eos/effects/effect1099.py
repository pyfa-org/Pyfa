# shipProjectileTrackingMF2
#
# Used by:
# Variations of ship: Slasher (3 of 3)
# Ship: Republic Fleet Firetail
# Ship: Wolf
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
