# Used by:
# Module: Reactive Armor Hardener
type = "active"
def handler(fit, module, context):
    for type in ("kinetic", "thermal", "explosive", "em"):
        attr = "armor%sDamageResonance" % type.capitalize()
        fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr),
                                  stackingPenalties=True, penaltyGroup="preMul")
