# shipBonusFrigateSizedMissileKineticDamageCD1
#
# Used by:
# Ship: Corax
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCD1"),
                                    skill="Caldari Destroyer")
