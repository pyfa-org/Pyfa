# reconShipCloakCpuBonus1
#
# Used by:
# Ships from group: Force Recon Ship (6 of 6)
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteBonusReconShip1") * level)
