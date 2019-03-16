# structureRigPDBCapacitorNeed
#
# Used by:
# Structure Modules from group: Structure Combat Rig L - Point Defense Battery Application and Projection (2 of 2)
# Structure Modules from group: Structure Combat Rig XL - Doomsday and Targeting (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Area Denial Module",
                                  "capacitorNeed", src.getModifiedItemAttr("structureRigPDCapUseBonus"),
                                  stackingPenalties=True)
