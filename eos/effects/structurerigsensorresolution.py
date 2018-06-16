# structureRigSensorResolution
#
# Used by:
# Structure Modules from group: Structure Combat Rig L - Max Targets and Sensor Boosting (2 of 2)
# Structure Modules from group: Structure Combat Rig M - Boosted Sensors (2 of 2)
# Structure Modules from group: Structure Combat Rig XL - Doomsday and Targeting (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("structureRigScanResBonus"),
                           stackingPenalties=True)
