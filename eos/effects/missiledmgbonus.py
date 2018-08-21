# missileDMGBonus
#
# Used by:
# Modules from group: Ballistic Control system (20 of 20)
type = "passive"


def handler(fit, container, context):
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "%sDamage" % dmgType,
                                           container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                           stackingPenalties=True)
