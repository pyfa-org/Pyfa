# shipbonusPCTTrackingPC2
#
# Used by:
# Ship: Vedmak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusPC2"), skill="Precursor Cruiser")
