# eliteBonusHeavyGunshipLaserDmg2
#
# Used by:
# Ship: Zealot
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"),
                                  skill="Heavy Assault Cruisers")
