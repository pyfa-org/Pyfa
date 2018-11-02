type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Precursor Weapon"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPD1"),
                                  skill="Precursor Destroyer")
