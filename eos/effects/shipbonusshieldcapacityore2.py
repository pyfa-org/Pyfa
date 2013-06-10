# Used by:
# Variations of ship: Procurer (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Booster",
                                  "shieldCapacity", ship.getModifiedItemAttr("shipBonusORE2") * level)
