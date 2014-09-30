# shipTCapNeedBonusAC
#
# Used by:
# Ships named like: Omen (3 of 4)
# Ship: Devoter
# Ship: Zealot
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAC") * level)
