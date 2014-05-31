# Used by:
# Variations of ship: Crucifier (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Weapon Disruption"),
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("shipBonus2AF") * level)
