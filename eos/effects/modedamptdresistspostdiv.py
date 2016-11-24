type = "passive"

def handler(fit, module, context):
    fit.ship.multiplyItemAttr("weaponDisruptionResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))
    fit.ship.multiplyItemAttr("sensorDampenerResistance", 1 / module.getModifiedItemAttr("modeEwarResistancePostDiv"))
