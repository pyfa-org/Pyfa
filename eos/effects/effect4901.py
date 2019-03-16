# shipMissileSpeedBonusAF
#
# Used by:
# Ship: Vengeance
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
