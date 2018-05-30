# structureRigEWMaxRangeFalloff
#
# Used by:
# Structure Modules from group: Structure Combat Rig M - EW projection (2 of 2)
# Structure Modules named like: Standup Set EW (4 of 4)
type = "passive"


def handler(fit, src, context):
    groups = ("Structure ECM Battery", "Structure Disruption Battery")

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "falloff", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "maxRange", src.getModifiedItemAttr("structureRigEwarOptimalBonus"),
                                  stackingPenalties=True)

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "falloffEffectiveness", src.getModifiedItemAttr("structureRigEwarFalloffBonus"),
                                  stackingPenalties=True)
