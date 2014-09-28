type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Missile Launcher Operation"),
                                  "speed", ship.getModifiedItemAttr("shipBonusAD1") * level)