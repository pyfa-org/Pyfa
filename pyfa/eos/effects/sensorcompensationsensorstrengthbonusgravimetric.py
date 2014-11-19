# sensorCompensationSensorStrengthBonusGravimetric
#
# Used by:
# Skill: Gravimetric Sensor Compensation
type = "passive"
def handler(fit, container, context):
    fit.ship.boostItemAttr("scanGravimetricStrength", container.getModifiedItemAttr("sensorStrengthBonus") * container.level)
