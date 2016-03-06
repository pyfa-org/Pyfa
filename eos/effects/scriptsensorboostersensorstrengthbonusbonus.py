type = "active"
def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
            module.boostItemAttr("scan{}StrengthPercent".format(scanType), module.getModifiedChargeAttr("sensorStrengthBonusBonus"))
