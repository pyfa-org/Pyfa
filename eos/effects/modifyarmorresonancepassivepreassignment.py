# Used by:
# Subsystems from group: Defensive Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    for type in ("Em", "Explosive", "Kinetic", "Thermal"):
        fit.ship.preAssignItemAttr("armor{0}DamageResonance".format(type), module.getModifiedItemAttr("passiveArmor{0}DamageResonance".format(type)))
