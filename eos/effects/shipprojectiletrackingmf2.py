# Used by:
# Variations of ship: Slasher (3 of 3)
# Ship: Jaguar
# Ship: Republic Fleet Firetail
# Ship: Wolf
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusMF2") * level)
