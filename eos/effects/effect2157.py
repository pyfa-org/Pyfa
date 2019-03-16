# eliteBonusCommandShipLaserDamageCS1
#
# Used by:
# Ship: Absolution
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips1"),
                                  skill="Command Ships")
