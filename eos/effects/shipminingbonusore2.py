# Used by:
# Variations of ship: Covetor (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Mining Barge").level
    groups = ("Strip Miner", "Frequency Mining Laser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "miningAmount", ship.getModifiedItemAttr("shipBonusORE2") * level)
