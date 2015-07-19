# dreadnoughtShipBonusLaserCapNeedA1
#
# Used by:
# Ship: Revelation
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"),
                                  "capacitorNeed", ship.getModifiedItemAttr("dreadnoughtShipBonusA1"), skill="Amarr Dreadnought")
