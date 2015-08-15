# eliteBonusElectronicAttackShipECMOptimalRange1
#
# Used by:
# Ship: Kitsune
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"), skill="Electronic Attack Ships")
