# subsystemBonusGallentePropulsion2Agility
#
# Used by:
# Subsystem: Proteus Propulsion - Hyperspatial Optimization
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                           skill="Gallente Propulsion Systems")
