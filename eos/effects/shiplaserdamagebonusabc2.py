# shipLaserDamageBonusABC2
#
# Used by:
# Ships named like: Harbinger (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusABC2"), skill="Amarr Battlecruiser")
