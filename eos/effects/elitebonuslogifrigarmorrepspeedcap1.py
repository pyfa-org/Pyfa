# eliteBonusLogiFrigArmorRepSpeedCap1
#
# Used by:
# Ship: Deacon
# Ship: Thalia
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "capacitorNeed", src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "duration", src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
