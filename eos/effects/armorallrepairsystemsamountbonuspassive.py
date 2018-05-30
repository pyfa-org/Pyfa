# armorAllRepairSystemsAmountBonusPassive
#
# Used by:
# Implants named like: Agency 'Hardshell' TB Dose (3 of 4)
# Implants named like: Exile Booster (4 of 4)
# Implant: Antipharmakon Kosybo
type = "passive"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Capital Repair Systems"),
        "armorDamageAmount", booster.getModifiedItemAttr("armorDamageAmountBonus") or 0)
