# eliteBonusCommandShipLaserROFCS2
#
# Used by:
# Ship: Absolution
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "speed", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
