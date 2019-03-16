# shipBonusHMLEMDamageAC
#
# Used by:
# Ship: Sacrilege
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "emDamage", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
