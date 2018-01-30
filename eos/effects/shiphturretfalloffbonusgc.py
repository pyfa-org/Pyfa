# shipHTurretFalloffBonusGC
#
# Used by:
# Ship: Victor
# Ship: Vigilant
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
