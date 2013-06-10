# Used by:
# Ship: Ragnarok
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Titan").level
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("titanMinmatarBonus4") * level)
