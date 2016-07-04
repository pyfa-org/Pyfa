# missileDMGBonus
#
# Used by:
# Modules from group: Ballistic Control system (17 of 17)
# Modules named like: QA Multiship Module Players (4 of 4)
type = "passive"
def handler(fit, module, context):
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "%sDamage" % dmgType, module.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                    stackingPenalties = True)
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties=True)
