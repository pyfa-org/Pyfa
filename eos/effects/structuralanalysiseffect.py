# Used by:
# Modules named like: Auxiliary Nano (8 of 8)
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Armor Implants > Implant Slot 09 (6 of 6)
# Implant: Imperial Navy Modified 'Noble' Implant
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", container.getModifiedItemAttr("repairBonus"),
                                  stackingPenalties = "implant" not in context)
