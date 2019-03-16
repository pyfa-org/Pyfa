type = "passive"


def handler(fit, module, context):
    secModifier = module.getModifiedItemAttr("securityModifier")
    module.multiplyItemAttr("structureRigDoomsdayDamageLossTargetBonus", secModifier)
    module.multiplyItemAttr("structureRigScanResBonus", secModifier)
    module.multiplyItemAttr("structureRigPDRangeBonus", secModifier)
    module.multiplyItemAttr("structureRigPDCapUseBonus", secModifier)
    module.multiplyItemAttr("structureRigMissileExploVeloBonus", secModifier)
    module.multiplyItemAttr("structureRigMissileVelocityBonus", secModifier)
    module.multiplyItemAttr("structureRigEwarOptimalBonus", secModifier)
    module.multiplyItemAttr("structureRigEwarFalloffBonus", secModifier)
    module.multiplyItemAttr("structureRigEwarCapUseBonus", secModifier)
    module.multiplyItemAttr("structureRigMissileExplosionRadiusBonus", secModifier)
    module.multiplyItemAttr("structureRigMaxTargetRangeBonus", secModifier)
