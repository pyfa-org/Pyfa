# Used by:
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Capital Industrial Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"),
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusORECapital3") * level)
