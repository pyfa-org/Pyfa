# Used by:
# Ship: Heretic
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusAD2") * level)
