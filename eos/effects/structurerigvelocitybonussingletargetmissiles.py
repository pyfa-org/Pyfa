# Not used by any item
type = "passive"


def handler(fit, src, context):
    groups = ("Structure Anti-Subcapital Missile", "Structure Anti-Capital Missile")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name in groups,
                                  "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                  stackingPenalties=True)
