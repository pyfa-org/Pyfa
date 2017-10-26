# shipBonusForceAuxiliaryG1RemoteShieldBoostAmount
#
# Used by:
# Ship: Loggerhead
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Shield Emission Systems"), "shieldBonus",
                                  src.getModifiedItemAttr("shipBonusForceAuxiliaryG1"), skill="Gallente Carrier")
