# subsystemBonusMinmatarDefensive2RemoteShieldTransporterAmount
#
# Used by:
# Subsystem: Loki Defensive - Adaptive Shielding
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Shield Booster",
                                  "shieldBonus", module.getModifiedItemAttr("subsystemBonusMinmatarDefensive2"), skill="Minmatar Defensive Systems")
