# subsystemBonusCaldariCore2MaxTargetingRange
#
# Used by:
# Subsystem: Tengu Core - Electronic Efficiency Gate
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
