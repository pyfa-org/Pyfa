# structureRigMaxTargets
#
# Used by:
# Structure Modules from group: Structure Combat Rig XL - Doomsday and Targeting (2 of 2)
# Structure Modules named like: Standup Set Target (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.extraAttributes.increase("maxTargetsLockedFromSkills", src.getModifiedItemAttr("structureRigMaxTargetBonus"))
