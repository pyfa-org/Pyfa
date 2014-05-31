type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosionDelay", ship.getModifiedItemAttr("shipBonusPirateFaction2"))
