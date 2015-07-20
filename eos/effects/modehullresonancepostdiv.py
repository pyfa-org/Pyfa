# modeHullResonancePostDiv
#
# Used by:
# Module: Hecate Defense Mode
type = "passive"
def handler(fit, module, context):
    for srcResType, tgtResType in (
        ("Em", "em"),
        ("Explosive", "explosive"),
        ("Kinetic", "kinetic"),
        ("Thermic", "thermal")
    ):
        fit.ship.multiplyItemAttr(
            "{0}DamageResonance".format(tgtResType),
            1 / module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(srcResType))
        )
