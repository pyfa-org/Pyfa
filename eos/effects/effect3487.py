# shipBonusSmallEnergyTurretDamagePirateFaction
#
# Used by:
# Ship: Caedes
# Ship: Confessor
# Ship: Cruor
# Ship: Imp
# Ship: Succubus
# Ship: Sunesis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
