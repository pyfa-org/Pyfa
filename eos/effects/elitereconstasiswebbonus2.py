# eliteReconStasisWebBonus2
#
# Used by:
# Ship: Huginn
# Ship: Moracha
# Ship: Rapier
# Ship: Victor
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
