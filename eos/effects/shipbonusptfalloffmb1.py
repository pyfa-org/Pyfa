# shipBonusPTFalloffMB1
#
# Used by:
# Ship: Marshal
# Ship: Vargur
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
