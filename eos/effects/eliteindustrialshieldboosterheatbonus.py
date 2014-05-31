# Used by:
# Ships from group: Deep Space Transport (4 of 4)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "overloadShieldBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "overloadSelfDurationBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
