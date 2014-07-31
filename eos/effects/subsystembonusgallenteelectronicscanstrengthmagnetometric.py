# Used by:
# Subsystem: Proteus Electronics - Dissolution Sequencer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Electronic Systems").level
    fit.ship.boostItemAttr("scanMagnetometricStrength", module.getModifiedItemAttr("subsystemBonusGallenteElectronic") * level)
