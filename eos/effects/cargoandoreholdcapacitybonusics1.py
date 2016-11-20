# cargoCapacityMultiply
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("specialOreHoldCapacity",
                           src.getModifiedItemAttr("shipBonusICS1"),
                           skill="Industrial Command Ships")

    fit.ship.boostItemAttr("capacity",
                           src.getModifiedItemAttr("shipBonusICS1"),
                           skill="Industrial Command Ships")
