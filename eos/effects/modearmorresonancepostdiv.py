type = "passive"
def handler(fit, module, context):
    for resType in ("Em", "Explosive", "Kinetic"):
        fit.ship.multiplyItemAttr("armor{0}DamageResonance".format(resType),
                            1/module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(resType)),
                            stackingPenalties = True, penaltyGroup="postDiv")

    # Thermal != Thermic
    fit.ship.multiplyItemAttr("armorThermalDamageResonance",
                            1/module.getModifiedItemAttr("modeThermicResistancePostDiv"),
                            stackingPenalties = True, penaltyGroup="postDiv")
