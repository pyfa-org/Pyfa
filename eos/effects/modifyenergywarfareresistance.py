type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("energyWarfareResistance",
                               module.getModifiedItemAttr("energyWarfareResistanceBonus"),
                               stackingPenalties = True
