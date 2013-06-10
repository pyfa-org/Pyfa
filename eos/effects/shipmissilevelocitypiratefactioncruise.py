# Used by:
# Ship: Rattlesnake
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusPirateFaction"))