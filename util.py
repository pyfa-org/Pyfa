def shorten(val, digits):
    if val > 10**8:
        return ("%." + str(digits)+ "fG") % (val / float(10**9))
    elif val > 10**6:
        return ("%." + str(digits)+ "fM") % (val / float(10**6))
    elif val > 10**3:
        return ("%." + str(digits)+ "fk") % (val / float(10**3))
    else:
        return ("%." + str(digits) + "f") % val
