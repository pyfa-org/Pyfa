# Not used by any item
type = "passive"


def handler(fit, module, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(type),
                               module.getModifiedItemAttr("subsystemBonusCaldariDefensive"),
                               skill="Caldari Defensive Systems")
