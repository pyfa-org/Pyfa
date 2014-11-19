# shipEnergyTCapNeedBonusAF
#
# Used by:
# Ship: Crusader
# Ship: Executioner
# Ship: Gold Magnate
# Ship: Retribution
# Ship: Silver Magnate
# Ship: Tormentor
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonus2AF") * level)
