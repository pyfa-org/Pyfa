# shipHTDmgBonusfixedGC
#
# Used by:
# Ship: Adrestia
# Ship: Arazu
# Ship: Deimos
# Ship: Enforcer
# Ship: Exequror Navy Issue
# Ship: Guardian-Vexor
# Ship: Thorax
# Ship: Vexor
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
