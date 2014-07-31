# Used by:
# Skill: Doomsday Operation
type = "passive"
def handler(fit, skill, context):
    damageTypes = ("em", "explosive", "kinetic", "thermal")
    for dmgType in damageTypes:
        dmgAttr = "{0}Damage".format(dmgType)
        fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Super Weapon" and dmgAttr in mod.itemModifiedAttributes,
                                      dmgAttr, skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
