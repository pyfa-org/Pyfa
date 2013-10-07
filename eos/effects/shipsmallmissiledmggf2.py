# Used by:
# Ship: Ares
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for damageType in damageTypes:
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets") or mod.charge.requiresSkill("Light Missiles"),
                                        "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusGF2") * level)
