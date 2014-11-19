# eliteBonusHeavyGunshipHeavyAndHeavyAssaultAndAssaultMissileLauncherROF
#
# Used by:
# Ship: Sacrilege
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Assault Cruisers").level
    groups = ("Missile Launcher Rapid Light", "Missile Launcher Heavy Assault", "Missile Launcher Heavy")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", ship.getModifiedItemAttr("eliteBonusHeavyGunship2") * level)
