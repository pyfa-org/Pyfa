# Used by:
# Ship: Phantasm
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusAC2") * level)
