# shipETOptimalRange2AF
#
# Used by:
# Ship: Imperial Navy Slicer
# Ship: Pacifier
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
