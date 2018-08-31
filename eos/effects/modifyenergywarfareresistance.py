# modifyEnergyWarfareResistance
#
# Used by:
# Modules from group: Capacitor Battery (30 of 30)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("energyWarfareResistance",
                           module.getModifiedItemAttr("energyWarfareResistanceBonus"),
                           stackingPenalties=True)
