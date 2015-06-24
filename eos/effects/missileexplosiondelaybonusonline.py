type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "explosionDelay", container.getModifiedItemAttr("explosionDelayBonus"),
                                    stackingPenalties=True)
