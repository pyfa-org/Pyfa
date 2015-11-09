# smallEnergyMaxRangeBonus
#
# Used by:
# Ship: Coercer
# Ship: Gold Magnate
# Ship: Silver Magnate
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("maxRangeBonus"))
