# shipBonusNosNeutCapNeedRoleBonus2
#
# Used by:
# Ship: Demavik
# Ship: Leshak
# Ship: Vedmak
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusRole2"))
