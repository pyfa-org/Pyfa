# shipModeSmallMissileDamagePostDiv
#
# Used by:
# Module: Jackdaw Sharpshooter Mode
type = "passive"


def handler(fit, module, context):
    for damage_type in ("thermal", "em", "explosive", "kinetic"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                        "{}Damage".format(damage_type), 1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"))
