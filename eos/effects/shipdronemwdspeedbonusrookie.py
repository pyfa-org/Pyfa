# shipDroneMWDSpeedBonusRookie
#
# Used by:
# Ship: Taipan
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda mod: True,
                                 "maxVelocity", ship.getModifiedItemAttr("rookieDroneMWDspeed"))
