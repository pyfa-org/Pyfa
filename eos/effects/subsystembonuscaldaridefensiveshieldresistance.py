# subsystemBonusCaldariDefensiveShieldResistance
#
# Used by:
# Subsystem: Tengu Defensive - Adaptive Shielding
type = "passive"


def handler(fit, module, context):
    for damage_type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.boostItemAttr("shield{0}DamageResonance".format(damage_type),
                               module.getModifiedItemAttr("subsystemBonusCaldariDefensive"),
                               skill="Caldari Defensive Systems")
