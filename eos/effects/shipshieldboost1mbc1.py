# Used by:
# Variations of ship: Cyclone (2 of 2)
# Ship: Cyclone Thukker Tribe Edition
# Ship: Sleipnir
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("shipBonusMBC1") * level)
