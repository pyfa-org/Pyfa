# eliteBonusGunshipHybridTracking2
#
# Used by:
# Ship: Enyo
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("eliteBonusGunship2"),
                                  skill="Assault Frigates")
