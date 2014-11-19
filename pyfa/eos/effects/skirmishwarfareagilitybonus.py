# skirmishWarfareAgilityBonus
#
# Used by:
# Implant: Federation Navy Warfare Mindlink
# Implant: Republic Fleet Warfare Mindlink
# Implant: Skirmish Warfare Mindlink
# Skill: Skirmish Warfare
type = "gang"
gangBoost = "agility"
gangBonus = "agilityBonus"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus) * level)
