# shipHybridDmgPirateCruiser
#
# Used by:
# Ship: Gnosis
# Ship: Vigilant
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
