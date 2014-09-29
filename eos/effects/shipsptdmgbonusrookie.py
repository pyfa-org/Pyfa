# shipSPTDmgBonusRookie
#
# Used by:
# Ship: Echo
# Ship: Reaper
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("rookieSPTDamageBonus"))
