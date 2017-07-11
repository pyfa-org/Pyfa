# subsystemBonusCaldariCoreScanStrengthGravimetric
#
# Used by:
# Subsystem: Tengu Core - Electronic Efficiency Gate
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanGravimetricStrength", src.getModifiedItemAttr("subsystemBonusCaldariCore"), skill="Caldari Core Systems")
