# Used by:
# Items from market group: Implants & Boosters > Implants > Skill Hardwiring > Electronic Systems Implants > Implant Slot 08 (6 of 6)
# Skill: Propulsion Jamming
type = "passive"
def handler(fit, container, context):
    groups = ("Stasis Web", "Warp Scrambler", "Warp Disrupt Field Generator")
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
