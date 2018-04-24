# shipbonusPCTOptimalPF2
#
# Used by:
# Ship: Demavik
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPF2"), skill="Precursor Frigate")
