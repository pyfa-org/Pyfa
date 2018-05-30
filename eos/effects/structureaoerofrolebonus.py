# structureAoERoFRoleBonus
#
# Used by:
# Items from category: Structure (11 of 14)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Guided Bomb Launcher",
                                  "speed", ship.getModifiedItemAttr("structureAoERoFRoleBonus"))
    for attr in ["duration", "durationTargetIlluminationBurstProjector", "durationWeaponDisruptionBurstProjector",
                 "durationECMJammerBurstProjector", "durationSensorDampeningBurstProjector", "capacitorNeed"]:
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Burst Projector",
                                      attr, ship.getModifiedItemAttr("structureAoERoFRoleBonus"))
