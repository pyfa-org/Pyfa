# shipSETDmgBonusAF
#
# Used by:
# Ship: Executioner
# Ship: Gold Magnate
# Ship: Silver Magnate
# Ship: Tormentor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
