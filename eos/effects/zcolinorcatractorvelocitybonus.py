# Used by:
# Ship: Orca
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", ship.getModifiedItemAttr("shipOrcaTractorBeamVelocityBonus2"))
