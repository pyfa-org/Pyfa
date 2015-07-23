# eliteBonusCommandShipProjectileFalloffCS2
#
# Used by:
# Ship: Sleipnir
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
