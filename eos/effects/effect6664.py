# skillBonusDroneSharpshooting
#
# Used by:
# Skill: Drone Sharpshooting
type = "passive"


def handler(fit, src, context):
    lvl = src.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxRange",
                                 src.getModifiedItemAttr("rangeSkillBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "fighterAbilityMissilesRange",
                                   src.getModifiedItemAttr("rangeSkillBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackTurretRangeOptimal",
                                   src.getModifiedItemAttr("rangeSkillBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"),
                                   "fighterAbilityAttackMissileRangeOptimal",
                                   src.getModifiedItemAttr("rangeSkillBonus") * lvl)
