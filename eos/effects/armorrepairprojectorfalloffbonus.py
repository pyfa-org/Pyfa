# armorRepairProjectorFalloffBonus
#
# Used by:
# Variations of ship: Navitas (2 of 2)
# Ship: Augoror
# Ship: Deacon
# Ship: Exequror
# Ship: Inquisitor
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer", "falloffEffectiveness", src.getModifiedItemAttr("falloffBonus"))
