# shipModeSmallMissileDamagePostDiv
#
# Used by:
# Module: Jackdaw Sharpshooter Mode
type = "passive"

def handler(fit, module, context):
    types = ("thermal", "em", "explosive", "kinetic")
    for type in types:
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                        "{}Damage".format(type), 1 / module.getModifiedItemAttr("modeDamageBonusPostDiv"))
