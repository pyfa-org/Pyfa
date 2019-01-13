# shipBonusNosNeutCapNeedRoleBonus2
#
# Used by:
# Ship: Rodiva
# Ship: Zarmazd
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"), "capacitorNeed", src.getModifiedItemAttr("shipBonusRole2"))
