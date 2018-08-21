# shipbonusPCTDamagePF1
#
# Used by:
# Ship: Damavik
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPF1"), skill="Precursor Frigate")
