# shipAdvancedSpaceshipCommandAgilityBonus
#
# Used by:
# Ships from group: Dreadnought (5 of 5)
# Ships from group: Titan (5 of 5)
# Items from market group: Ships > Capital Ships (32 of 32)
type = "passive"


def handler(fit, ship, context):
    skillName = "Advanced Spaceship Command"
    skill = fit.character.getSkill(skillName)
    fit.ship.boostItemAttr("agility", skill.getModifiedItemAttr("agilityBonus"), skill=skillName)
