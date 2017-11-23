# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxRange",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"), skill="Minmatar Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxTractorVelocity",
                                  src.getModifiedItemAttr("subsystemBonusMinmatarDefensive3"), skill="Minmatar Defensive Systems")
