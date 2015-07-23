# shipSETDamageAmarrTacticalDestroyer1
#
# Used by:
# Ship: Confessor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr1"), skill="Amarr Tactical Destroyer")
