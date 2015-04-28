# eliteBonusMarauderShieldBonus2a
#
# Used by:
# Ship: Golem
# Ship: Vargur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("eliteBonusViolators2") * level)
