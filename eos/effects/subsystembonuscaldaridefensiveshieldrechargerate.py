# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldRechargeRate", module.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                           skill="Caldari Defensive Systems")
