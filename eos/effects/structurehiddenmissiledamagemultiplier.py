# structureHiddenMissileDamageMultiplier
#
# Used by:
# Items from category: Structure (14 of 14)
type = "passive"


def handler(fit, src, context):
    groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.item.group.name in groups,
                                           "%sDamage" % dmgType,
                                           src.getModifiedItemAttr("hiddenMissileDamageMultiplier"))
