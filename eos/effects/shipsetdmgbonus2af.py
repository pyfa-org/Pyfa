# shipSETDmgBonus2AF
#
# Used by:
# Ship: Punisher
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
