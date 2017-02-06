# shipModeSPTDamagePostDiv
#
# Used by:
# Module: Svipul Sharpshooter Mode
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
        lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
        "damageMultiplier",
        1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
