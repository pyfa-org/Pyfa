# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Transfer Array",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAC") * level)
