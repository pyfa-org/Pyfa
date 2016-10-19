# eliteBonusElectronicAttackShipWarpScramblerCapNeed2
#
# Used by:
# Ship: Keres
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2"),
                                  skill="Electronic Attack Ships")
