# shipBonusLightMissileAllDamageMC2
#
# Used by:
# Ship: Rapier
# Ship: Scythe Fleet Issue
type = "passive"
def handler(fit, ship, context):
    for damageType in ("em", "explosive", "kinetic", "thermal"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                        "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusMC2"), skill="Minmatar Cruiser")
