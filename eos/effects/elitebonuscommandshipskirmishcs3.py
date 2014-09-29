# eliteBonusCommandShipSkirmishCS3
#
# Used by:
# Ships from group: Command Ship (4 of 8)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Warfare Specialist"),
                                  "commandBonus", ship.getModifiedItemAttr("eliteBonusCommandShips3") * level)
