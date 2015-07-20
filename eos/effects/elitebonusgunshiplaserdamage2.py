# eliteBonusGunshipLaserDamage2
#
# Used by:
# Ship: Retribution
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")