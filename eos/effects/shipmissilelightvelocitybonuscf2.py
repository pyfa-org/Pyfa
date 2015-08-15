# shipMissileLightVelocityBonusCF2
#
# Used by:
# Ship: Caldari Navy Hookbill
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
