# shipBonusTorpedoVelocityGF2
#
# Used by:
# Ship: Nemesis
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
