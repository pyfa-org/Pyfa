# shipHeavyMissileKinDmgPirateCruiser
#
# Used by:
# Ship: Gnosis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusRole7"))
