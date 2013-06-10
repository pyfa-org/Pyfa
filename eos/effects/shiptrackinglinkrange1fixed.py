# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tracking Link",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMC") * level)
