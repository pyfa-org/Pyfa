type = "passive"
def handler(fit, src, context):
    for module in fit.modules:
        if module.getModifiedItemAttr("lightningWeaponDamageLossTarget"):
            boostAmount = 1+src.getModifiedItemAttr("structureRigDoomsdayDamageLossTargetBonus")
            module.multiplyItemAttr("lightningWeaponDamageLossTarget",boostAmount)
