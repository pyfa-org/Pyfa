# Used by:
# Subsystems from group: Electronic Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    sensorTypes = ("Gravimetric", "Ladar", "Magnetometric", "Radar")
    for sensorType in sensorTypes:
        sensAttr = "scan{0}Strength".format(sensorType)
        fit.ship.increaseItemAttr(sensAttr, module.getModifiedItemAttr(sensAttr))
