# Used by:
# Modules from group: Ballistic Control system (21 of 21)
# Modules named like: QA Multiship Module Players (4 of 4)
type = "passive"
def handler(fit, container, context):
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "%sDamage" % dmgType, container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                    stackingPenalties = True)