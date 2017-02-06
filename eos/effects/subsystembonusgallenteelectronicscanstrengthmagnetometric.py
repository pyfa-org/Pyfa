# subsystemBonusGallenteElectronicScanStrengthMagnetometric
#
# Used by:
# Subsystem: Proteus Electronics - Dissolution Sequencer
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanMagnetometricStrength", module.getModifiedItemAttr("subsystemBonusGallenteElectronic"),
                           skill="Gallente Electronic Systems")
