# Not used by any item
type = "passive"
runTime = "early"


def handler(fit, src, context):

    for attr in [
        "structureRigDoomsdayDamageLossTargetBonus",
        "structureRigScanResBonus",
        "structureRigPDRangeBonus",
        "structureRigPDCapUseBonus",
        "structureRigMissileExploVeloBonus",
        "structureRigMissileVelocityBonus",
        "structureRigEwarOptimalBonus",
        "structureRigEwarFalloffBonus",
        "structureRigEwarCapUseBonus",
        "structureRigMissileExplosionRadiusBonus"
    ]:
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Jury Rigging"),
                                  attr, src.getModifiedItemAttr("structureRoleBonus"))
