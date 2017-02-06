# shipModeSHTDamagePostDiv
#
# Used by:
# Module: Hecate Sharpshooter Mode
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
        lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
        "damageMultiplier",
        1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
