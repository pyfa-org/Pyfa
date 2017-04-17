# shipHeavyAssaultMissileExpDmgPirateCruiser
#
# Used by:
# Ship: Gnosis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusRole7"))
