# skillStructureMissileDamageBonus
#
# Used by:
# Skill: Structure Missile Systems
type = "passive", "structure"


def handler(fit, src, context):
    groups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile", "Structure Guided Bomb")
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                        "%sDamage" % damageType, src.getModifiedItemAttr("damageMultiplierBonus"),
                                        skill="Structure Missile Systems")
