# eliteBonusHeavyGunshipDroneControlRange1
#
# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    fit.extraAttributes.increase("droneControlRange", ship.getModifiedItemAttr("eliteBonusHeavyGunship1"), skill="Heavy Assault Cruisers")
