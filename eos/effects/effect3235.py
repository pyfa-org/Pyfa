# shipRocketKineticDmgAF
#
# Used by:
# Ship: Anathema
# Ship: Vengeance
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
