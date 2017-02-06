# missileBombardmentMaxFlightTimeBonusPostPercentExplosionDelayOwnerCharModulesRequiringMissileLauncherOperation
#
# Used by:
# Implants named like: Zainou 'Deadeye' Missile Bombardment MB (6 of 6)
# Modules named like: Rocket Fuel Cache Partition (8 of 8)
# Implant: Antipharmakon Toxot
# Skill: Missile Bombardment
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    penalized = False if "skill" in context or "implant" in context or "booster" in context else True
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosionDelay", container.getModifiedItemAttr("maxFlightTimeBonus") * level,
                                    stackingPenalties=penalized)
