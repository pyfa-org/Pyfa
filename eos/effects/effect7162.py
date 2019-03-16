# shipRoleDisintegratorMaxRangeCBC
#
# Used by:
# Ship: Drekavac
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Precursor Weapon"),
                                  "maxRange", ship.getModifiedItemAttr("roleBonusCBC"))
