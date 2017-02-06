# cargoAndOreHoldCapacityBonusICS1
#
# Used by:
# Ships from group: Industrial Command Ship (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("specialOreHoldCapacity",
                           src.getModifiedItemAttr("shipBonusICS1"),
                           skill="Industrial Command Ships")

    fit.ship.boostItemAttr("capacity",
                           src.getModifiedItemAttr("shipBonusICS1"),
                           skill="Industrial Command Ships")
