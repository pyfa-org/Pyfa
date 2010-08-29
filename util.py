def shorten(val, digits):
    if val > 10**10:
        return ("%." + str(digits)+ "fG") % (val / float(10**9))
    elif val > 10**7:
        return ("%." + str(digits)+ "fM") % (val / float(10**6))
    elif val > 10**4:
        return ("%." + str(digits)+ "fk") % (val / float(10**3))
    else:
        return ("%." + str(digits) + "f") % val
