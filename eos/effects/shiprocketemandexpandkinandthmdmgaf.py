# Used by:
# Ship: Malediction
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Frigate").level
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for damageType in damageTypes:
        fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                        "{0}Damage".format(damageType), ship.getModifiedItemAttr("shipBonusAF") * level)
