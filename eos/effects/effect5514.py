# eliteBonusCommandShipHeavyAssaultMissileDamageCS2
#
# Used by:
# Ship: Damnation
type = "passive"


def handler(fit, ship, context):
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for damageType in damageTypes:
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "{0}Damage".format(damageType),
                                        ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
