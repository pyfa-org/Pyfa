# shipHeavyAssaultMissileEMAndExpAndKinAndThmDmgAC1
#
# Used by:
# Ship: Sacrilege
type = "passive"
def handler(fit, ship, context):
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for damageType in damageTypes:
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Assault Missiles"),
                                        "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
