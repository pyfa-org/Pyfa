# shipSmallMissileDmgPirateFaction
#
# Used by:
# Ship: Jackdaw
type = "passive"
def handler(fit, ship, context):
    for damageType in ("em", "explosive", "kinetic", "thermal"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                        "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusPirateFaction"))
