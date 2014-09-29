# carrierFighterControlRangeBonus
#
# Used by:
# Ships from group: Carrier (4 of 4)
# Ships from group: Supercarrier (5 of 5)
type = "passive"
def handler(fit, ship, context):
    # The fighter control range bonus only affects fighters.
    # Until we can calculate and display control range on a per-drone level,
    # we will have to leave this effect as a dummy.
    pass
    # fit.extraAttributes.multiply("droneControlRange", ship.getModifiedItemAttr("droneRangeBonus"))
