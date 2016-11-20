# carrierCaldariDroneMax1
#
# Used by:
# Ship: Chimera
# Ship: Wyvern
type = "passive"


def handler(fit, ship, context):
    fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("carrierCaldariBonus1"),
                                 skill="Caldari Carrier")
