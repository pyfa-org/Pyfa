# roleBonusTorpRoF1
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo", "speed", src.getModifiedItemAttr("shipBonusRole1"))
