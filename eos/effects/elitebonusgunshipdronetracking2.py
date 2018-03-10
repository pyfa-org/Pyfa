# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed",
                                 src.getModifiedItemAttr("eliteBonusGunship2"), stackingPenalties=True, skill="Assault Frigates")
