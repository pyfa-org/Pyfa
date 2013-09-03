# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusCC") * level)
