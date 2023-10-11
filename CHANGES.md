# What I changed

well, it took me ages to figure out the requirements for m1 macs, but here we go!

1. i switched to conda (anaconda3-2023.07-2). then you can actually install most of the original reqs even on m1. environment.yml

2. change pyfa.spec a variable, remove git if you want to build the .app package locally etc:

after this you need to update the preferences panel as we are using 4.1.1 wxpython instead of 4.0.6 and there were some changes regarding sizer

pyfaGeneralPreferences.py

PFGeneralPref.register()

and finally modify the osx-package.sh script to accommodate these changes and use the conda virtual env we've created