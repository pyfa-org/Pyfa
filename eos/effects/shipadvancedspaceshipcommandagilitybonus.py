# shipAdvancedSpaceshipCommandAgilityBonus
#
# Used by:
# Items from market group: Ships > Capital Ships (32 of 34)
type = "passive"
def handler(fit, ship, context):
    skill = fit.character.getSkill("Advanced Spaceship Command")
    fit.ship.boostItemAttr("agility", skill.getModifiedItemAttr("agilityBonus") * skill.level)
