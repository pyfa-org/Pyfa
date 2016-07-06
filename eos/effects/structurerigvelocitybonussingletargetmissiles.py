type = "passive"
def handler(fit, src, context):
    groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
    fit.modules.filteredChargeMultiply(lambda mod: mod.charge.group.name in groups,
                                       "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                       stackingPenalties=True)
