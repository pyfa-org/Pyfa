# Used by:
# Ship: Sentinel
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Electronic Attack Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Destabilizer",
                                  "energyDestabilizationRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1") * level)
