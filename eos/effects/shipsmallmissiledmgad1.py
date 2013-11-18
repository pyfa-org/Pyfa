# Used by:
# Ship: Heretic
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Destroyer").level
    for damageType in ("em", "thermal", "explosive", "kinetic"):
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                        "%sDamage" % damageType, ship.getModifiedItemAttr("shipBonusAD1") * level)
