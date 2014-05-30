type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "overloadSpeedFactorBonus", ship.getModifiedItemAttr("roleBonusOverheatDST"))
