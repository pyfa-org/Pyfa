# shipbonusPCTOptimalPF2
#
# Used by:
# Ship: Damavik
# Ship: Hydra
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusPF2"), skill="Precursor Frigate")
