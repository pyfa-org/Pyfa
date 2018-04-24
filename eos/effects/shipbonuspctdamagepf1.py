# shipbonusPCTDamagePF1
#
# Used by:
# Ship: Demavik
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPF1"), skill="Precursor Frigate")
