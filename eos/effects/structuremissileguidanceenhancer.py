# Not used by any item
type = "passive"


def handler(fit, container, context):
    missileGroups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile")
    for srcAttr, tgtAttr in (
            ("aoeCloudSizeBonus", "aoeCloudSize"),
            ("aoeVelocityBonus", "aoeVelocity"),
            ("missileVelocityBonus", "maxVelocity"),
            ("explosionDelayBonus", "explosionDelay"),
    ):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in missileGroups,
                                        tgtAttr, container.getModifiedItemAttr(srcAttr),
                                        stackingPenalties=True)
