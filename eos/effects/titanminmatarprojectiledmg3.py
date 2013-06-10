# Used by:
# Ship: Ragnarok
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Titan").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("titanMinmatarBonus3") * level)
