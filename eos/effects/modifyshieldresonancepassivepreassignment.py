# Not used by any item
type = "passive"


def handler(fit, module, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.preAssignItemAttr("shield{0}DamageResonance".format(type),
                                   module.getModifiedItemAttr("passiveShield{0}DamageResonance".format(type)))
