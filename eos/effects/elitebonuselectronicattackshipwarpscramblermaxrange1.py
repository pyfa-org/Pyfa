# eliteBonusElectronicAttackShipWarpScramblerMaxRange1
#
# Used by:
# Ship: Keres
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                  skill="Electronic Attack Ships")
