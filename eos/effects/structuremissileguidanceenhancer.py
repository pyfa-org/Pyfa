# structureMissileGuidanceEnhancer
#
# Used by:
# Variations of structure module: Standup Missile Guidance Enhancer I (2 of 2)
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
