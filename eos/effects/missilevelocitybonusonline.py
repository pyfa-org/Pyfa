type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", container.getModifiedItemAttr("missileVelocityBonus"),
                                    stackingPenalties=True)
