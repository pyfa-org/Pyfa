# eliteBonusGunshipHybridOptimal1
#
# Used by:
# Ship: Enyo
# Ship: Harpy
# Ship: Ishkur
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")