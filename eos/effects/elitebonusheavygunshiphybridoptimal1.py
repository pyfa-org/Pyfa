# eliteBonusHeavyGunshipHybridOptimal1
#
# Used by:
# Ship: Eagle
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1") * level)
