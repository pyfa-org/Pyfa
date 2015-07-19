# shipBonusTorpedoVelocityCF2
#
# Used by:
# Ship: Manticore
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCF2"), skill="Caldari Frigate")
