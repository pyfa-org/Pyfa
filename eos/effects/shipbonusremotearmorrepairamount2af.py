# shipBonusRemoteArmorRepairAmount2AF
#
# Used by:
# Ship: Deacon
# Ship: Inquisitor
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"), "armorDamageAmount", src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
