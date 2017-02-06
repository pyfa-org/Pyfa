# shipCapPropulsionJamming
#
# Used by:
# Ships from group: Interceptor (10 of 10)
# Ship: Atron
# Ship: Condor
# Ship: Executioner
# Ship: Slasher
type = "passive"


def handler(fit, ship, context):
    groups = ("Stasis Web", "Warp Scrambler")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "capacitorNeed", ship.getModifiedItemAttr("eliteBonusInterceptorRole"))
