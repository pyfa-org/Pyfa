# eliteBonusInterdictorsProjectileFalloff1
#
# Used by:
# Ship: Sabre
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusInterdictors1"), skill="Interdictors")
