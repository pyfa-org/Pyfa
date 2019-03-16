# subsystemBonusMinmatarPropulsion2Agility
#
# Used by:
# Subsystem: Loki Propulsion - Intercalated Nanofibers
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                           skill="Minmatar Propulsion Systems")
