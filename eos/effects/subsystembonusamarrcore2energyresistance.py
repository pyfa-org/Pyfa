# subsystemBonusAmarrCore2EnergyResistance
#
# Used by:
# Subsystem: Legion Core - Augmented Antimatter Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")
