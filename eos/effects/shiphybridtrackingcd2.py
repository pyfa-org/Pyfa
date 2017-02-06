# shipHybridTrackingCD2
#
# Used by:
# Ship: Cormorant
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusCD2"), skill="Caldari Destroyer")
