# structureRigDoomsdayDamageLoss
#
# Used by:
# Structure Modules from group: Structure Combat Rig XL - Doomsday and Targeting (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                     "lightningWeaponDamageLossTarget",
                                     src.getModifiedItemAttr("structureRigDoomsdayDamageLossTargetBonus"))
