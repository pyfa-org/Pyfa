# shipBonusMF1TorpedoExplosionVelocity
#
# Used by:
# Ship: Hound
# Ship: Virtuoso
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeVelocity", ship.getModifiedItemAttr("shipBonusMF"), skill="Minmatar Frigate")
