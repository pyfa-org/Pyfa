# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Structure Guided Bomb",
                                    "maxVelocity", src.getModifiedItemAttr("structureRigMissileVelocityBonus"),
                                    stackingPenalties=True)
