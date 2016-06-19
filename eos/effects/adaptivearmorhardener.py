# adaptiveArmorHardener
#
# Used by:
# Module: Reactive Armor Hardener
type = "active"
def handler(fit, module, context):
    for type in ("kinetic", "thermal", "explosive", "em"):
        attr = "armor%sDamageResonance" % type.capitalize()

        #Adjust RAH to match the current damage pattern
        damagePattern = fit.damagePattern
        attrDamagePattern = "%sAmount" % type
        damagePatternModifier = getattr(damagePattern,attrDamagePattern)/float(sum((damagePattern.emAmount,damagePattern.thermalAmount,damagePattern.kineticAmount,damagePattern.explosiveAmount)))
        modifiedResistModifier = (1-(((1-module.getModifiedItemAttr(attr))*4)*(damagePatternModifier)))
        module.forceItemAttr(attr, modifiedResistModifier)

        fit.ship.multiplyItemAttr(attr, module.getModifiedItemAttr(attr),
                                  stackingPenalties=True, penaltyGroup="preMul")
