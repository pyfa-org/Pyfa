# Used by:
# Implants named like: Zainou Defender Missiles (6 of 6)
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Defender Missiles"),
                                       "maxVelocity", container.getModifiedItemAttr("missileVelocityBonus"))