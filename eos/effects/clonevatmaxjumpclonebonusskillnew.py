# Used by:
# Skill: Cloning Facility Operation
type = "passive"
def handler(fit, skill, context):
    fit.ship.boostItemAttr("maxJumpClones", skill.getModifiedItemAttr("maxJumpClonesBonus") * skill.level)
