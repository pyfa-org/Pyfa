# structureRigExplosionRadiusBonusAoEMissiles
#
# Used by:
# Structure Modules from group: Structure Combat Rig L - AoE Launcher Application and Projection (2 of 2)
# Structure Modules from group: Structure Combat Rig XL - Missile and AoE Missile (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                    "aoeCloudSize", src.getModifiedItemAttr("structureRigMissileExplosionRadiusBonus"),
                                    stackingPenalties=True)
