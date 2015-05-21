# shipModeMissileVelocityPostDiv
#
# Used by:
# Module: Jackdaw Sharpshooter Mode
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredChargeMultiply(
        lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
        "maxVelocity",
        1 / module.getModifiedItemAttr("modeMaxRangePostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
