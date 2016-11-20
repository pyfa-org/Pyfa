# shipWebVelocityBonusRookie
#
# Used by:
# Ship: Hematos
# Ship: Violator
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "speedFactor", ship.getModifiedItemAttr("rookieWebAmount"))
