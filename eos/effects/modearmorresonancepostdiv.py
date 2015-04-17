# modeArmorResonancePostDiv
#
# Used by:
# Modules named like: Defense Mode (2 of 2)
type = "passive"
def handler(fit, module, context):
    for srcResType, tgtResType in (
        ("Em", "Em"),
        ("Explosive", "Explosive"),
        ("Kinetic", "Kinetic"),
        ("Thermic", "Thermal")
    ):
        fit.ship.multiplyItemAttr(
            "armor{0}DamageResonance".format(tgtResType),
            1 / module.getModifiedItemAttr("mode{0}ResistancePostDiv".format(srcResType)),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )
