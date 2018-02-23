# Not used by any item
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
