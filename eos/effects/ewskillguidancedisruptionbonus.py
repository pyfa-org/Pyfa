type = "passive"
def handler(fit, src, context):
    level = src.level if "skill" in context else 1
    for attr in (
        "explosionDelayBonus",
        "aoeVelocityBonus",
        "aoeCloudSizeBonus",
        "missileVelocityBonus"
    ):
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                      attr, src.getModifiedItemAttr("scanSkillEwStrengthBonus") * level)