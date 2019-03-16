# eliteBonusLogiFrigShieldRepSpeedCap1
#
# Used by:
# Ship: Kirin
# Ship: Scalpel
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "duration",
                                  src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"), "capacitorNeed",
                                  src.getModifiedItemAttr("eliteBonusLogiFrig1"), skill="Logistics Frigates")
