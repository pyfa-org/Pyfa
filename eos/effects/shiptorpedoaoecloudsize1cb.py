# shipTorpedoAOECloudSize1CB
#
# Used by:
# Ship: Raven Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
