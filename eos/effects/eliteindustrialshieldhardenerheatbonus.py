type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Tactical Shield Manipulation"),
                                  "overloadHardeningBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
