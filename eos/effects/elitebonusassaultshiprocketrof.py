# Used by:
# Ship: Cambion
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Assault Frigates").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rocket",
                                  "speed", ship.getModifiedItemAttr("eliteBonusGunship1") * level)
