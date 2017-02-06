# shipArmorHpAC2
#
# Used by:
# Ship: Augoror Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorHP", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
