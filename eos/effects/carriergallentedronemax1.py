# carrierGallenteDroneMax1
#
# Used by:
# Ship: Nyx
# Ship: Thanatos
type = "passive"


def handler(fit, ship, context):
    fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("carrierGallenteBonus1"),
                                 skill="Gallente Carrier")
