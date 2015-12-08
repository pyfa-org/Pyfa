# shipEnergyTCapNeedBonusAF
#
# Used by:
# Ship: Crusader
# Ship: Executioner
# Ship: Gold Magnate
# Ship: Punisher
# Ship: Retribution
# Ship: Silver Magnate
# Ship: Tormentor
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
