# Used by:
# Ship: Keres
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Electronic Attack Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip2") * level)