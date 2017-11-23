# subsystemBonusMinmatarCore2MaxTargetingRange
#
# Used by:
# Subsystem: Loki Core - Dissolution Sequencer
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"),
                           skill="Minmatar Core Systems")
