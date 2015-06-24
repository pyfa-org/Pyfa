type = "active"
def handler(fit, container, context):
    for srcAttr, tgtAttr, penalize in (
        ("aoeCloudSizeBonus", "aoeCloudSize", False),
        ("aoeVelocityBonus", "aoeVelocity", False),
        ("missileVelocityBonus", "maxVelocity", True),
        ("explosionDelayBonus", "explosionDelay", True),
    ):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                        tgtAttr, container.getModifiedItemAttr(srcAttr),
                                        stackingPenalties=penalize)
