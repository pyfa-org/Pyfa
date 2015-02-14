# shipSPTDamageMinmatarTacticalDestroyer1
#
# Used by:
# Ship: Svipul
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar1") * level)
