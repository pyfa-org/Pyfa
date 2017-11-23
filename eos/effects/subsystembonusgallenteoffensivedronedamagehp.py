# subsystemBonusGallenteOffensiveDroneDamageHP
#
# Used by:
# Subsystem: Proteus Offensive - Drone Synthesis Projector
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "armorHP", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                 skill="Gallente Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "hp", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                 skill="Gallente Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "damageMultiplier", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                 skill="Gallente Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"),
                                 "shieldCapacity", src.getModifiedItemAttr("subsystemBonusGallenteOffensive"),
                                 skill="Gallente Offensive Systems")
