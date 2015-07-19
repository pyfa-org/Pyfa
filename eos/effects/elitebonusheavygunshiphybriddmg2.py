# eliteBonusHeavyGunshipHybridDmg2
#
# Used by:
# Ship: Deimos
# Ship: Eagle
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusHeavyGunship2"), skill="Heavy Assault Cruisers")
