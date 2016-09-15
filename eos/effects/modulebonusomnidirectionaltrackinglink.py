# moduleBonusOmnidirectionalTrackingLink
#
# Used by:
# Modules from group: Drone Tracking Modules (10 of 10)
type = "active"
def handler(fit, src, context):
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretRangeFalloff", src.getModifiedItemAttr("falloffBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesExplosionVelocity", src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "trackingSpeed", src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileExplosionRadius", src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretTrackingSpeed", src.getModifiedItemAttr("trackingSpeedBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesExplosionRadius", src.getModifiedItemAttr("aoeCloudSizeBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange", src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "falloff", src.getModifiedItemAttr("falloffBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileExplosionVelocity", src.getModifiedItemAttr("aoeVelocityBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackMissileRangeFalloff", src.getModifiedItemAttr("falloffBonus"), stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange", src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityAttackTurretRangeOptimal", src.getModifiedItemAttr("maxRangeBonus"), stackingPenalties=True)
