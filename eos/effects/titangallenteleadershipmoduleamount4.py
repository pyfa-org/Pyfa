# Used by:
# Ship: Erebus
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Titan").level
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                  "maxGroupActive", ship.getModifiedItemAttr("titanGallenteBonus4") * level)
