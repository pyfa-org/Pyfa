# shipPCBSDmgBonusPCBS2
#
# Used by:
# Ship: Leshak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusPBS2"), skill="Precursor Battleship")
