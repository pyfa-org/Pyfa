# Used by:
# Ship: Caldari Navy Hookbill
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCF2") * level)
