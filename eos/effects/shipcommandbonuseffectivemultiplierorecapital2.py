# shipCommandBonusEffectiveMultiplierOreCapital2
#
# Used by:
# Ship: Rorqual
type = "passive"


def handler(fit, ship, context):
    if fit.extraAttributes["siege"]:
        fit.ship.increaseItemAttr("commandBonusEffective", ship.getModifiedItemAttr("shipBonusORECapital2"),
                                  skill="Capital Industrial Ships")
