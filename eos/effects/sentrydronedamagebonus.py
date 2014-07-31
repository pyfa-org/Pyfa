# Used by:
# Modules named like: Sentry Damage Augmentor (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "damageMultiplier", module.getModifiedItemAttr("damageMultiplierBonus"),
                                 stackingPenalties = True)