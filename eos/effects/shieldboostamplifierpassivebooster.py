# shieldBoostAmplifierPassiveBooster
#
# Used by:
# Implants named like: Agency 'Hardshell' TB Dose (4 of 4)
# Implants named like: Blue Pill Booster (5 of 5)
# Implant: Antipharmakon Thureo
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(
        lambda mod: mod.item.requiresSkill("Shield Operation") or mod.item.requiresSkill("Capital Shield Operation"),
        "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))
