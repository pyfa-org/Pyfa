type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Hull Upgrades"),
                                  "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
