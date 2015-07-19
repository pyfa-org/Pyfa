# eliteBonusHeavyGunshipLaserOptimal1
#
# Used by:
# Ship: Zealot
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"), skill="Heavy Assault Cruisers")
