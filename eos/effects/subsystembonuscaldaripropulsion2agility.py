# subsystemBonusCaldariPropulsion2Agility
#
# Used by:
# Subsystem: Tengu Propulsion - Chassis Optimization
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                           skill="Caldari Propulsion Systems")
