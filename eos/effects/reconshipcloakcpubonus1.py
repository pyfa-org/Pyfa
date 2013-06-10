# Used by:
# Ships from group: Force Recon Ship (4 of 4)
type = "passive"
runTime = "early"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cloaking Device",
                                  "cpu", ship.getModifiedItemAttr("eliteBonusReconShip1") * level)
