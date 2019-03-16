# shipHTDmgBonusGB
#
# Used by:
# Ship: Dominix Navy Issue
# Ship: Hyperion
# Ship: Kronos
# Ship: Marshal
# Ship: Megathron Federate Issue
# Ship: Sin
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB"),
                                  skill="Gallente Battleship")
