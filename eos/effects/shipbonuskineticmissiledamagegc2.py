# shipBonusKineticMissileDamageGC2
#
# Used by:
# Ship: Chameleon
# Ship: Gila
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
