# Used by:
# Skill: Armored Warfare
type = "gang"
gangBoost = "armorHP"
gangBonus = "armorHpBonus"
def handler(fit, skill, context):
    fit.ship.boostItemAttr(gangBoost, skill.getModifiedItemAttr(gangBonus) * skill.level)
