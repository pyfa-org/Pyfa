'''
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Structure Doomsday Weapon", "lightningWeaponTargetAmount", src.getModifiedItemAttr("structureRigDoomsdayTargetAmountBonus"), stackingPenalties=True)
    # This is all wrong.  We need to modify the module attached to the ship (citadel) and add the bonus from the rig.
    # So Rig -> Ship -> Module
'''

type = "passive"
def handler(fit, src, context):
    for module in fit.modules:
        if module.getModifiedItemAttr("lightningWeaponTargetAmount"):
            module.increaseItemAttr("lightningWeaponTargetAmount",src.getModifiedItemAttr("structureRigDoomsdayTargetAmountBonus"))
