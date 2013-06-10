# Used by:
# Ship: Blackbird
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCC2") * level)
