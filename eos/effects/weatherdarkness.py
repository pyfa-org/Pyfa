# weather_darkness
#
# Used by:
# Celestial: darkness_weather_1
# Celestial: darkness_weather_2
# Celestial: darkness_weather_3
runTime = "early"
type = ("projected", "passive", "gang")


def handler(fit, beacon, context, **kwargs):
    for x in range(1, 3):
        if beacon.getModifiedItemAttr("warfareBuff{}ID".format(x)):
            value = beacon.getModifiedItemAttr("warfareBuff{}Value".format(x))
            id = beacon.getModifiedItemAttr("warfareBuff{}ID".format(x))

            if id:
                fit.addCommandBonus(id, value, beacon, kwargs['effect'], 'early')
