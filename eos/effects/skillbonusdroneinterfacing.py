# skillBonusDroneInterfacing
#
# Used by:
# Implants from group: Cyber Drones (2 of 2)
# Skill: Drone Interfacing
type = "passive"


def handler(fit, src, context):
    lvl = src.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                 src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackMissileDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackTurretDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityMissilesDamageMultiplier",
                                   src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"), "miningDroneAmountPercent",
                                 src.getModifiedItemAttr("miningAmountBonus") * lvl)
