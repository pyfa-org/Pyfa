# Used by:
# Ship: Falcon
# Ship: Rook
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Recon Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "scanRadarStrengthBonus", ship.getModifiedItemAttr("eliteBonusReconShip2") * level)
