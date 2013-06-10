# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Logistics").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Transporter",
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusLogistics2") * level)
