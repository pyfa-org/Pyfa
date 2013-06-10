# Used by:
# Ship: Phoenix
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Dreadnought").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Citadel Torpedoes"),
                                    "kineticDamage", ship.getModifiedItemAttr("dreadnoughtShipBonusC2") * level)
