# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", ship.getModifiedItemAttr("commandBonusEffective"))
