# subsystemBonusAmarrCoreCapacitorCapacity
#
# Used by:
# Subsystem: Legion Core - Augmented Antimatter Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("capacitorCapacity", src.getModifiedItemAttr("subsystemBonusAmarrCore"), skill="Amarr Core Systems")
