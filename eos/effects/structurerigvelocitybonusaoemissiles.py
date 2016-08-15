type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                     "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                     stackingPenalties=True)
