# Used by:
# Ship: Harbinger Navy Issue

type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusABC1") * level)
