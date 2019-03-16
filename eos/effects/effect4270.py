# subsystemBonusMinmatarCore3ScanResolution
#
# Used by:
# Subsystem: Loki Core - Dissolution Sequencer
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanResolution", src.getModifiedItemAttr("subsystemBonusMinmatarCore3"),
                           skill="Minmatar Core Systems")
