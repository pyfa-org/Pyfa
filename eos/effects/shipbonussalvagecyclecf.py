# Used by:
# Ship: Heron
# Ship: Sukuuvestaa Heron
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Salvaging"),
                                  "duration", ship.getModifiedItemAttr("shipBonusCF") * level)
