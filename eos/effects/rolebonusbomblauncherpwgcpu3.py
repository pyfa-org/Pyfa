# roleBonusBombLauncherPWGCPU3
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"), "power", src.getModifiedItemAttr("shipBonusRole3"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Bomb Deployment"), "cpu", src.getModifiedItemAttr("shipBonusRole3"))
