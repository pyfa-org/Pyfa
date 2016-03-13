# droneDamageBonusOnline
#
# Used by:
# Modules from group: Drone Damage Modules (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", module.getModifiedItemAttr("droneDamageBonus"),
                                 stackingPenalties = True)
