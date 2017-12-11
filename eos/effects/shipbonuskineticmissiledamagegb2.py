# shipBonusKineticMissileDamageGB2
#
# Used by:
# Ship: Rattlesnake
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusGB2"),
                                    skill="Gallente Battleship")
