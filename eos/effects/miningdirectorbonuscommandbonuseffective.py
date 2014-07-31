# Used by:
# Ships from group: Capital Industrial Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", ship.getModifiedItemAttr("commandBonusEffective"))
