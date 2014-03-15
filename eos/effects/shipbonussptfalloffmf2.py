# Used by:
# Ships named like: Rifter (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusMF2") * level)
