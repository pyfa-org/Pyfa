# shipBonusTorpedoVelocity2AF
#
# Used by:
# Ship: Purifier
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
