# titanMinmatarProjectileDmg3
#
# Used by:
# Ship: Ragnarok
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanMinmatarBonus3"), skill="Minmatar Titan")
