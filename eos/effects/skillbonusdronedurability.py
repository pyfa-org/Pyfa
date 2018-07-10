# skillBonusDroneDurability
#
# Used by:
# Implant: CreoDron 'Bumblebee' Drone Tuner T10-5D
# Implant: CreoDron 'Yellowjacket' Drone Tuner D5-10T
# Skill: Drone Durability
type = "passive"


def handler(fit, src, context):
    lvl = src.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                 src.getModifiedItemAttr("hullHpBonus") * lvl)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                 src.getModifiedItemAttr("armorHpBonus") * lvl)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                 src.getModifiedItemAttr("shieldCapacityBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                   src.getModifiedItemAttr("shieldCapacityBonus") * lvl)
