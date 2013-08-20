# Used by:
# Ship: Basilisk
# Ship: Etana
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Logistics").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics1") * level)
