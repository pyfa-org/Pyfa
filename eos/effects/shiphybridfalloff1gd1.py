# shipHybridFallOff1GD1
#
# Used by:
# Variations of ship: Catalyst (6 of 7)
# Ship: Catalyst Serpentis Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGD1") * level)
