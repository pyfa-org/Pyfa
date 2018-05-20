# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                     "lightningWeaponDamageLossTarget",
                                     src.getModifiedItemAttr("structureRigDoomsdayDamageLossTargetBonus"))
