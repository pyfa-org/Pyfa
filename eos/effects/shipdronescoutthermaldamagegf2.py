# Used by:
# Ship: Helios
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Scout Drone Operation"),
                                 "thermalDamage", ship.getModifiedItemAttr("shipBonusGF2") * level)
