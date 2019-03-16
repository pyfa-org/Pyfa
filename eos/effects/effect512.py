# shipSHTDmgBonusGF
#
# Used by:
# Variations of ship: Incursus (3 of 3)
# Ship: Atron
# Ship: Federation Navy Comet
# Ship: Helios
# Ship: Pacifier
# Ship: Taranis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
