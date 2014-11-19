# missileDMGBonusPassive
#
# Used by:
# Modules named like: Warhead Calefaction Catalyst (8 of 8)
type = "passive"
def handler(fit, container, context):
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                           "%sDamage" % dmgType, container.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                           stackingPenalties = True)