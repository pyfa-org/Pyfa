# skirmishWarfareAgilityBonusReplacer
#
# Used by:
# Implant: Federation Navy Warfare Mindlink
# Implant: Republic Fleet Warfare Mindlink
# Implant: Skirmish Warfare Mindlink
type = "gang"
gangBoost = "agility"
gangBonus = "agilityBonus"
def handler(fit, container, context):
    fit.ship.boostItemAttr(gangBoost, container.getModifiedItemAttr(gangBonus))
