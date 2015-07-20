# eliteBonusGunshipLaserOptimal1
#
# Used by:
# Ship: Retribution
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")