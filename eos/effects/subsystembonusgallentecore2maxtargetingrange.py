# subsystemBonusGallenteCore2MaxTargetingRange
#
# Used by:
# Subsystem: Proteus Core - Electronic Efficiency Gate
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("maxTargetRange", src.getModifiedItemAttr("subsystemBonusGallenteCore2"),
                           skill="Gallente Core Systems")
