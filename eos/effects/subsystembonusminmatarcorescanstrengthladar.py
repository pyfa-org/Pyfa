# subsystemBonusMinmatarCoreScanStrengthLADAR
#
# Used by:
# Subsystem: Loki Core - Dissolution Sequencer
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanLadarStrength", src.getModifiedItemAttr("subsystemBonusMinmatarCore"),
                           skill="Minmatar Core Systems")
