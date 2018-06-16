# structureBallisticControlSystem
#
# Used by:
# Variations of structure module: Standup Ballistic Control System I (2 of 2)
type = "passive"


def handler(fit, module, context):
    missileGroups = ("Structure Anti-Capital Missile", "Structure Anti-Subcapital Missile")

    for dmgType in ("em", "kinetic", "explosive", "thermal"):
        fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name in missileGroups,
                                           "%sDamage" % dmgType,
                                           module.getModifiedItemAttr("missileDamageMultiplierBonus"),
                                           stackingPenalties=True)

    launcherGroups = ("Structure XL Missile Launcher", "Structure Multirole Missile Launcher")
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name in launcherGroups,
                                     "speed", module.getModifiedItemAttr("speedMultiplier"),
                                     stackingPenalties=True)
