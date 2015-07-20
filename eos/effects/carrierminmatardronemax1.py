# carrierMinmatarDroneMax1
#
# Used by:
# Ship: Hel
# Ship: Nidhoggur
type = "passive"
def handler(fit, ship, context):
    fit.extraAttributes.increase("maxActiveDrones", ship.getModifiedItemAttr("carrierMinmatarBonus1"), skill="Minmatar Carrier")
