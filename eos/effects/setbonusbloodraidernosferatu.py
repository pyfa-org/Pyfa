# setBonusBloodraiderNosferatu
#
# Used by:
# Implants named like: grade Talisman (15 of 18)
type = "passive"


def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capacitor Emission Systems"),
                                  "duration", implant.getModifiedItemAttr("durationBonus"))
