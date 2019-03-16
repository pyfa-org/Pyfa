# weather_electric_storm
#
# Used by:
# Celestial: electric_storm_weather_1
# Celestial: electric_storm_weather_2
# Celestial: electric_storm_weather_3
runTime = "early"
type = ("projected", "passive", "gang")


def handler(fit, beacon, context, **kwargs):
    for x in range(1, 3):
        if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
            value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')
