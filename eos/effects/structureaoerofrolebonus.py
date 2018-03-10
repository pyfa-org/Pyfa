# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Guided Bomb Launcher",
                                  "speed", ship.getModifiedItemAttr("structureAoERoFRoleBonus"))
    for attr in ["duration", "durationTargetIlluminationBurstProjector", "durationWeaponDisruptionBurstProjector",
                 "durationECMJammerBurstProjector", "durationSensorDampeningBurstProjector", "capacitorNeed"]:
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Burst Projector",
                                      attr, ship.getModifiedItemAttr("structureAoERoFRoleBonus"))
