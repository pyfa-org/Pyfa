# Used by:
# Ship: Orca
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Industrial Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Director"),
                                  "commandBonus", ship.getModifiedItemAttr("shipOrcaForemanBonus") * level)
