# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"), stackingPenalties=True, skill="Caldari Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"), skill="Caldari Defensive Systems")
