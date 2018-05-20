# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("subsystemBonusMinmatarDefensive"),
                           skill="Minmatar Defensive Systems")
