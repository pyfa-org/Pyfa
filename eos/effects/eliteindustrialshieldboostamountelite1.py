# Used by:
# Ship: Bustard
# Ship: Crane
# Ship: Mastodon
# Ship: Prowler
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Transport Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", ship.getModifiedItemAttr("eliteBonusIndustrial1") * level)
