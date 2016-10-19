# moduleBonusInformationWarfareLinkSensorIntegrity
#
# Used by:
# Variations of module: Information Warfare Link - Sensor Integrity I (2 of 2)
type = "gang", "active"
gangBoost = "maxTargetRange"
gangBonus = "commandBonus"


# runTime = "late"

def handler(fit, module, context):
    if "gang" not in context:
          return
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("commandBonus"),
                           stackingPenalties=True)
    for scanType in ("Gravimetric", "Radar", "Ladar", "Magnetometric"):
        fit.ship.boostItemAttr("scan%sStrength" % scanType,
                               module.getModifiedItemAttr("commandBonus"),
                               stackingPenalties=True)
