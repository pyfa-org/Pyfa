# eliteBonusGunshipShieldBoost2
#
# Used by:
# Ship: Hawk
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")
