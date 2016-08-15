type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                     "aoeCloudSize", src.getModifiedItemAttr("structureRigMissileExplosionRadiusBonus"),
                                     stackingPenalties=True)
