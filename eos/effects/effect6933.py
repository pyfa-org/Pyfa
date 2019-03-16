# subsystemBonusCaldariCore2EnergyResistance
#
# Used by:
# Subsystem: Tengu Core - Augmented Graviton Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusCaldariCore2"),
                           skill="Caldari Core Systems")
