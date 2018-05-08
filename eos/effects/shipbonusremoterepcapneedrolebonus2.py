# shipBonusRemoteRepCapNeedRoleBonus2
#
# Used by:
# Ship: Damavik
# Ship: Leshak
# Ship: Vedmak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusRole2"))
