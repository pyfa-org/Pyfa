# shipBonusAoeVelocityRocketsCD2
#
# Used by:
# Ship: Corax
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusCD2") * level)
