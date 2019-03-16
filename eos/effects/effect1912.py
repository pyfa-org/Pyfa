# eliteReconBonusMagnetometricStrength2
#
# Used by:
# Ship: Chameleon
# Ship: Falcon
# Ship: Rook
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "scanMagnetometricStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2"),
                                  skill="Recon Ships")
