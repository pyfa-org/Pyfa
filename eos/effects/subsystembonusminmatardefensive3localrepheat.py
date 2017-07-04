type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Shield Operation"),
                                  "overloadArmorDamageAmount", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"),
                                  skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Shield Operation"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"),
                                  skill="Minmatar Defensive Systems")

