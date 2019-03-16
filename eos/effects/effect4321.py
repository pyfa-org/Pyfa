# subsystemBonusCaldariCore2ECMStrengthRange
#
# Used by:
# Subsystem: Tengu Core - Obfuscation Manifold
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanLadarStrengthBonus",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanRadarStrengthBonus",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "maxRange",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanGravimetricStrengthBonus",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "scanMagnetometricStrengthBonus",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore2"), skill="Caldari Core Systems")
