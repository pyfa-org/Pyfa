# modifyEnergyWarfareResistance
#
# Used by:
# Modules from group: Capacitor Battery (22 of 22)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("energyWarfareResistance",
                               module.getModifiedItemAttr("energyWarfareResistanceBonus"),
                               stackingPenalties = True)
