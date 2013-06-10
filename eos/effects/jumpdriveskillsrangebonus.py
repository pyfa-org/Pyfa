# Used by:
# Skill: Jump Drive Calibration
type = "passive"
def handler(fit, skill, context):
    fit.ship.boostItemAttr("jumpDriveRange", skill.getModifiedItemAttr("jumpDriveRangeBonus") * skill.level)