# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusRole2"))
