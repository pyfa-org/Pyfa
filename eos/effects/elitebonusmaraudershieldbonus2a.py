# eliteBonusMarauderShieldBonus2a
#
# Used by:
# Ships from group: Marauder (8 of 16)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("eliteBonusViolators2") * level)
