# eliteReconScramblerRangeBonus2
#
# Used by:
# Ship: Arazu
# Ship: Enforcer
# Ship: Lachesis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
