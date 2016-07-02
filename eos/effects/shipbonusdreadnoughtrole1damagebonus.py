# shipBonusDreadnoughtRole1DamageBonus
#
# Used by:
# Ship: Vehement (used to be used by Naglfar)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole1"))

