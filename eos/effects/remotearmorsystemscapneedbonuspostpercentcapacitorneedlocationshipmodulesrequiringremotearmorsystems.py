# remoteArmorSystemsCapNeedBonusPostPercentCapacitorNeedLocationShipModulesRequiringRemoteArmorSystems
#
# Used by:
# Implants named like: Inherent Implants 'Noble' Remote Armor Repair Systems RA (6 of 6)
# Modules named like: Remote Repair Augmentor (6 of 8)
# Skill: Remote Armor Repair Systems
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "capacitorNeed", container.getModifiedItemAttr("capNeedBonus") * level)
