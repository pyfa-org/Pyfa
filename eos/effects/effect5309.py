# shipHybridFallOff1GD1
#
# Used by:
# Ship: Catalyst
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
