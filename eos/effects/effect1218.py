# shipBonusPirateSmallHybridDmg
#
# Used by:
# Ship: Daredevil
# Ship: Hecate
# Ship: Sunesis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
