# structureRigNeutralizerCapacitorNeed
#
# Used by:
# Structure Modules from group: Structure Combat Rig XL - Energy Neutralizer and EW (2 of 2)
# Structure Modules named like: Standup Set Energy Neutralizer (4 of 6)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Energy Neutralizer",
                                  "capacitorNeed", src.getModifiedItemAttr("structureRigEwarCapUseBonus"),
                                  stackingPenalties=True)
