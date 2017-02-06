# eliteBonusGunshipHybridDmg2
#
# Used by:
# Ship: Harpy
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                  skill="Assault Frigates")
