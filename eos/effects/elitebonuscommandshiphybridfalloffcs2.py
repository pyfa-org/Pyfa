# eliteBonusCommandShipHybridFalloffCS2
#
# Used by:
# Ship: Astarte
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
