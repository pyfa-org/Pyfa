# shipTCapNeedBonusAC
#
# Used by:
# Ship: Devoter
# Ship: Omen
# Ship: Zealot
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusAC") * level)
