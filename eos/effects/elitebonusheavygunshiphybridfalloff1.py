# eliteBonusHeavyGunshipHybridFallOff1
#
# Used by:
# Ship: Deimos
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"), skill="Heavy Assault Cruisers")
