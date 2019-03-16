# shipBonusPirateFrigateProjDamage
#
# Used by:
# Ship: Chremoas
# Ship: Dramiel
# Ship: Sunesis
# Ship: Svipul
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
