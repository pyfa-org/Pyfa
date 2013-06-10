# Used by:
# Ship: Corax
# Ship: Gila
# Ship: Talwar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusPirateFaction"))
