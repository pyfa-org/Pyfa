# eliteBonusCommandShipMediumHybridDamageCS2
#
# Used by:
# Ship: Vulture
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
