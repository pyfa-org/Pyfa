# shipHybridDmg1CBC2
#
# Used by:
# Ship: Ferox
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCBC2"),
                                  skill="Caldari Battlecruiser")
