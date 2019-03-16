# shipBonusDroneTrackingEliteGunship2
#
# Used by:
# Ship: Ishkur
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed",
                                 src.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")
