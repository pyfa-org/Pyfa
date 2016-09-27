type = "passive"
def handler(fit, src, context):
    for module in fit.modules:
        if module.getModifiedItemAttr("lightningWeaponTargetAmount"):
            module.increaseItemAttr("lightningWeaponTargetAmount",src.getModifiedItemAttr("structureRigDoomsdayTargetAmountBonus"))
