# shipModeSPTTrackingPostDiv
#
# Used by:
# Module: Svipul Sharpshooter Mode
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
        lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
        "trackingSpeed",
        1 / module.getModifiedItemAttr("modeTrackingPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
