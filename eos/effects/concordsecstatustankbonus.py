# concordSecStatusTankBonus
#
# Used by:
# Ship: Enforcer
# Ship: Pacifier
type = "passive"


def handler(fit, src, context):

    # Get pilot sec status bonus directly here, instead of going through the intermediary effects
    # via https://forums.eveonline.com/default.aspx?g=posts&t=515826
    try:
        bonus = max(0, min(50.0, (src.parent.character.secStatus * 10)))
    except:
        bonus = None

    if bonus is not None:
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", bonus, stackingPenalties=True)
        fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", bonus, stackingPenalties=True)
