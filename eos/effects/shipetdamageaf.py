# shipETDamageAF
#
# Used by:
# Ship: Crusader
# Ship: Imperial Navy Slicer
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")