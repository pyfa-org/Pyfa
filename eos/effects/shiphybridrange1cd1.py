# shipHybridRange1CD1
#
# Used by:
# Ship: Cormorant
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCD1"), skill="Caldari Destroyer")
