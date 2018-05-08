# shipPCBSSPeedBonusPCBS1
#
# Used by:
# Ship: Leshak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Precursor Weapon"),
                                  "speed", ship.getModifiedItemAttr("shipBonusPBS1"), skill="Precursor Battleship")
