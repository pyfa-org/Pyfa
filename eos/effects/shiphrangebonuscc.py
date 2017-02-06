# shipHRangeBonusCC
#
# Used by:
# Ship: Eagle
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
