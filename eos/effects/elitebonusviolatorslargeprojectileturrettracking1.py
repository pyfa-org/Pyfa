# Used by:
# Ship: Vargur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Marauders").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusViolators1") * level)
