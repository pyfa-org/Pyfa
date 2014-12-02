type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Tactical Destroyer").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Energy Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusTacticalDestroyerAmarr1") * level)
