# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("scanGravimetricStrength", module.getModifiedItemAttr("subsystemBonusCaldariElectronic"),
                           skill="Caldari Electronic Systems")
