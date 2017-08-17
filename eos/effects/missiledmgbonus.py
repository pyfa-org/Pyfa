# missileDMGBonus
#
# Used by:
# Modules from group: Ballistic Control system (18 of 18)
type = "passive"


def handler(fit, container, context):
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "%sDamage" % dmgType,
                                           container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                           stackingPenalties=True)
