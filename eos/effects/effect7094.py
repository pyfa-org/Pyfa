# shipBonusRemoteRepMaxRangeRoleBonus1
#
# Used by:
# Ship: Damavik
# Ship: Drekavac
# Ship: Hydra
# Ship: Kikimora
# Ship: Leshak
# Ship: Tiamat
# Ship: Vedmak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusRole1"))
