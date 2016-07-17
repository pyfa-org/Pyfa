# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
displayName = "Energy Neutralizer"
prefix = "fighterAbilityEnergyNeutralizer"
type = "active", "projected"


def handler(fit, src, context):
    if "projected" in context:
        amount = src.getModifiedItemAttr("{}Amount".format(prefix))
        time = src.getModifiedItemAttr("{}Duration".format(prefix))
        rigSize = fit.ship.getModifiedItemAttr("rigSize")
        modifierLarge = src.getModifiedItemAttr("entityCapacitorLevelModifierLarge")
        modifierMedium = src.getModifiedItemAttr("entityCapacitorLevelModifierMedium")
        modifierSmall = src.getModifiedItemAttr("entityCapacitorLevelModifierSmall")
        energyNeutralizerSignatureResolution = src.getModifiedItemAttr("energyNeutralizerSignatureResolution")
        signatureRadius = fit.ship.getModifiedItemAttr("signatureRadius")

        #Signature reduction, uses the bomb formula as per CCP Larrikin
        if energyNeutralizerSignatureResolution:
            sigRatio = signatureRadius/energyNeutralizerSignatureResolution

            sigReductionList = [1, sigRatio]
            amount = amount*min(sigReductionList)

        # Small rigged ships
        if (rigSize == 1) and modifierSmall:
            amount = amount * modifierSmall

        # Medium rigged ships
        if (rigSize == 2) and modifierMedium:
            amount = amount * modifierMedium

        # Large rigged ships
        if (rigSize == 3) and modifierLarge:
            amount = amount * modifierLarge

        fit.addDrain(time, amount, 0)