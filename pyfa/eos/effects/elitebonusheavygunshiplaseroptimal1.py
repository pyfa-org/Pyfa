# eliteBonusHeavyGunshipLaserOptimal1
#
# Used by:
# Ship: Zealot
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1") * level)
