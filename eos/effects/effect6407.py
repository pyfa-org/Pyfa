# structureRigEWCapacitorNeed
#
# Used by:
# Structure Modules from group: Structure Combat Rig M - EW Cap Reduction (2 of 2)
# Structure Modules named like: Standup Set EW (4 of 4)
type = "passive"


def handler(fit, src, context):
    groups = ("Structure ECM Battery", "Structure Disruption Battery")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                  stackingPenalties=True)
