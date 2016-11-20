# carrierAmarrDroneMax1
#
# Used by:
# Ship: Aeon
# Ship: Archon
type = "passive"


def handler(fit, ship, context):
    fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("carrierAmarrBonus1"),
                                 skill="Amarr Carrier")
