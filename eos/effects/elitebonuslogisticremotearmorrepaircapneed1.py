# Used by:
# Ship: Oneiros
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Logistics").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Projector",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics1") * level)
