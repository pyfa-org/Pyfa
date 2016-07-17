# energyNeutralizerFalloff
#
# Used by:
# Modules from group: Energy Neutralizer (51 of 51)
from eos.types import State
type = "active", "projected"


def handler(fit, src, context):
    if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or hasattr(src, "amountActive")):
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")
        time = src.getModifiedItemAttr("duration")
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
