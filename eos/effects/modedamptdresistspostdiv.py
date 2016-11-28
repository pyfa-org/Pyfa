# modeDampTDResistsPostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (4 of 4)
type = "passive"

def handler(fit, module, context):
    fit.ship.multiplyItemAttr("weaponDisruptionResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))
    fit.ship.multiplyItemAttr("sensorDampenerResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))
