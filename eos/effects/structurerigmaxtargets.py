# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.extraAttributes.increase("maxTargetsLockedFromSkills", src.getModifiedItemAttr("structureRigMaxTargetBonus"))
