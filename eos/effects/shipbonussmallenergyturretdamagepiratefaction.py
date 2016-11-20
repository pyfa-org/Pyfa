# shipBonusSmallEnergyTurretDamagePirateFaction
#
# Used by:
# Ship: Confessor
# Ship: Cruor
# Ship: Imp
# Ship: Succubus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
