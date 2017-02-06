# shipSPTDamageMinmatarTacticalDestroyer1
#
# Used by:
# Ship: Svipul
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar1"),
                                  skill="Minmatar Tactical Destroyer")
