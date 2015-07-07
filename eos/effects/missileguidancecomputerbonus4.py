# missileGuidanceComputerBonus4
#
# Used by:
# Modules from group: Missile Guidance Computer (3 of 3)
type = "active"
def handler(fit, container, context):
    for srcAttr, tgtAttr in (
        ("aoeCloudSizeBonus", "aoeCloudSize"),
        ("aoeVelocityBonus", "aoeVelocity"),
        ("missileVelocityBonus", "maxVelocity"),
        ("explosionDelayBonus", "explosionDelay"),
    ):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        tgtAttr, container.getModifiedItemAttr(srcAttr),
                                        stackingPenalties=True)
