type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPBC1"),
                                  skill="Precursor Battlecruiser")
