import os, glob
import msgfmt

import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
locale_path = os.path.abspath(os.path.join(script_dir, '..', 'locale'))

for name in glob.iglob(locale_path + '/**'):
    if not os.path.isfile(name):
        path = os.path.join(locale_path, name, 'LC_MESSAGES', 'lang')
        sys.argv[1:] = [path + '.po']
        msgfmt.reset()
        msgfmt.main()
