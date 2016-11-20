# shipBonusHeavyMissileEMDmgMB
#
# Used by:
# Ship: Typhoon Fleet Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "emDamage", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
