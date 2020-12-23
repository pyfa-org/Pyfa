import gettext
gettext.install('lang', './locale')
gettext.translation('lang', './locale', languages=['zh_CH']).install(True)
print(_("Sample Title Text English"))