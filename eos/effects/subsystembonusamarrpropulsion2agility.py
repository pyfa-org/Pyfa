# subsystemBonusAmarrPropulsion2Agility
#
# Used by:
# Subsystem: Legion Propulsion - Intercalated Nanofibers
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                           skill="Amarr Propulsion Systems")
