# moduleBonusDroneDamageAmplifier
#
# Used by:
# Modules from group: Drone Damage Modules (11 of 11)
type = "passive"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesDamageMultiplier", src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretDamageMultiplier", src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileDamageMultiplier", src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier", src.getModifiedItemAttr("droneDamageBonus"), stackingPenalties=True)
