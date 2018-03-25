# boosterArmorHpPenalty
#
# Used by:
# Implants from group: Booster (12 of 62)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Armor Capacity"

# Attribute that this effect targets
attr = "boosterArmorHPPenalty"


def handler(fit, booster, context):
    fit.ship.boostItemAttr("armorHP", booster.getModifiedItemAttr(attr))
