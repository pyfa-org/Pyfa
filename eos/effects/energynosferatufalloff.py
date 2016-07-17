# energyNosferatuFalloff
#
# Used by:
# Modules from group: Energy Nosferatu (51 of 51)
type = "active", "projected"
runTime = "late"
def handler(fit, module, context):
    amount = module.getModifiedItemAttr("powerTransferAmount")
    time = module.getModifiedItemAttr("duration")
    rigSize = fit.ship.getModifiedItemAttr("rigSize")
    modifierLarge = module.getModifiedItemAttr("entityCapacitorLevelModifierLarge")
    modifierMedium = module.getModifiedItemAttr("entityCapacitorLevelModifierMedium")
    modifierSmall = module.getModifiedItemAttr("entityCapacitorLevelModifierSmall")
    energyNeutralizerSignatureResolution = module.getModifiedItemAttr("energyNeutralizerSignatureResolution")
    signatureRadius = fit.ship.getModifiedItemAttr("signatureRadius")

    if "projected" in context:
        # Signature reduction, uses the bomb formula as per CCP Larrikin
        if energyNeutralizerSignatureResolution:
            sigRatio = signatureRadius / energyNeutralizerSignatureResolution

            sigReductionList = [1, sigRatio]
            amount = amount * min(sigReductionList)

        #Small rigged ships
        if (rigSize == 1) and modifierSmall:
            amount = amount*modifierSmall

        #Medium rigged ships
        if (rigSize == 2) and modifierMedium:
            amount = amount*modifierMedium

        #Large rigged ships
        if (rigSize == 3) and modifierLarge:
            amount = amount*modifierLarge

        fit.addDrain(time, amount, 0)
    elif "module" in context:
        module.itemModifiedAttributes.force("capacitorNeed", -amount)