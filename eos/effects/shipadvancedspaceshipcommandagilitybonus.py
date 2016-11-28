# shipAdvancedSpaceshipCommandAgilityBonus
#
# Used by:
# Items from market group: Ships > Capital Ships (34 of 34)
type = "passive"


def handler(fit, ship, context):
    skillName = "Advanced Spaceship Command"
    skill = fit.character.getSkill(skillName)
    fit.ship.boostItemAttr("agility", skill.getModifiedItemAttr("agilityBonus"), skill=skillName)
