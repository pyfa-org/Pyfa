# Shield Command Boost
#
# Used by:
# Orca
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("buffDuration",
                           src.getModifiedItemAttr("shipBonusICS3"),
                           skill="Industrial Command Ships",
                           )
    fit.ship.boostItemAttr("warfareBuff1Value",
                           src.getModifiedItemAttr("shipBonusICS3"),
                           skill="Industrial Command Ships",
                           )
    fit.ship.boostItemAttr("warfareBuff2Value",
                           src.getModifiedItemAttr("shipBonusICS3"),
                           skill="Industrial Command Ships",
                           )
    fit.ship.boostItemAttr("warfareBuff3Value",
                           src.getModifiedItemAttr("shipBonusICS3"),
                           skill="Industrial Command Ships",
                           )
    fit.ship.boostItemAttr("warfareBuff4Value",
                           src.getModifiedItemAttr("shipBonusICS3"),
                           skill="Industrial Command Ships",
                           )

#  TODO: test
