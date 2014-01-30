# Used by:
# Ship: Stratios
# Ship: Stratios Emergency Responder
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPirateFaction"))
