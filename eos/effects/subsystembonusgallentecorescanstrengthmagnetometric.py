# subsystemBonusGallenteCoreScanStrengthMagnetometric
#
# Used by:
# Subsystem: Proteus Core - Electronic Efficiency Gate
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("scanMagnetometricStrength", src.getModifiedItemAttr("subsystemBonusGallenteCore"),
                           skill="Gallente Core Systems")
