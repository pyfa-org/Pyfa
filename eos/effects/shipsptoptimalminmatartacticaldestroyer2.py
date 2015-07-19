# shipSPTOptimalMinmatarTacticalDestroyer2
#
# Used by:
# Ship: Svipul
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusTacticalDestroyerMinmatar2"), skill="Minmatar Tactical Destroyer")
