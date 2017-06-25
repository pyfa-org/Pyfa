# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "scanMagnetometricStrengthBonus",
                                  module.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                  skill="Caldari Offensive Systems")
