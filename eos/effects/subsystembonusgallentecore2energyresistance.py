# subsystemBonusGallenteCore2EnergyResistance
#
# Used by:
# Subsystem: Proteus Core - Augmented Fusion Reactor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("energyWarfareResistance", src.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                           skill="Gallente Core Systems")
