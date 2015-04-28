# shipBonusMiningDurationORE3
#
# Used by:
# Ships from group: Exhumer (3 of 3)
# Ships from group: Mining Barge (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "duration", ship.getModifiedItemAttr("shipBonusORE3") * level)
