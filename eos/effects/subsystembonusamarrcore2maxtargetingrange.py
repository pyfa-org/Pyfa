# subsystemBonusAmarrCore2MaxTargetingRange
#
# Used by:
# Subsystem: Legion Core - Dissolution Sequencer
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusAmarrCore2"),
                           skill="Amarr Core Systems")
