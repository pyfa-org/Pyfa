# shipbonusPCTDamagePC1
#
# Used by:
# Ship: Vedmak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPC1"), skill="Precursor Cruiser")
