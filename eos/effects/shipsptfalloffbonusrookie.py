# shipSPTFalloffBonusRookie
#
# Used by:
# Ship: Echo
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("rookieSPTFalloff"))
