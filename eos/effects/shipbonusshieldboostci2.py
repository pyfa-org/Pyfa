# shipBonusShieldBoostCI2
#
# Used by:
# Ship: Bustard
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Industrial").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusCI2") * level)
