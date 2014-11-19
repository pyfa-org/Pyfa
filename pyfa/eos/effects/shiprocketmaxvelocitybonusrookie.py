# shipRocketMaxVelocityBonusRookie
#
# Used by:
# Ship: Taipan
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "maxVelocity", ship.getModifiedItemAttr("rookieRocketVelocity"))
