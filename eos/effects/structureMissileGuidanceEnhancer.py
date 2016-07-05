# missileAOECloudSizeBonusOnline
#
# Used by:
# Modules from group: Missile Guidance Enhancer (3 of 3)
type = "passive"
def handler(fit, module, context):
    groups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "aoeCloudSize", module.getModifiedItemAttr("aoeCloudSizeBonus"),
                                    stackingPenalties=True)
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "aoeVelocity", module.getModifiedItemAttr("aoeVelocityBonus"),
                                    stackingPenalties=True)
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "explosionDelay", module.getModifiedItemAttr("explosionDelayBonus"),
                                    stackingPenalties=True)
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                    "maxVelocity", module.getModifiedItemAttr("missileVelocityBonus"),
                                    stackingPenalties=True)