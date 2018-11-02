# shipBonusPD2DisintegratorMaxRange
#
# Used by:
# Ship: Kikimora
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPD2"),
                                  skill="Precursor Destroyer")
