# shipProjectileRofPirateCruiser
#
# Used by:
# Ship: Cynabal
# Ship: Moracha
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusRole7"))
