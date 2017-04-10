"""
    2017/04/05: unread description tests module.
"""
# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))

import re
#
# noinspection PyPackageRequirements
from _development.helpers import DBInMemory as DB, Gamedata, Saveddata
# noinspection PyPep8
from service.port import Port, IPortUser

# from utils.strfunctions import sequential_rep, replace_ltgt
from utils.stopwatch import Stopwatch

"""
NOTE:
  description character length is restricted 4hundred by EVE client.
  these things apply to multi byte environment too.


    o read xml fit data (and encode to utf-8 if need.

    o construct xml dom object, and extract "fitting" elements.

    o apply _resolve_ship method to each "fitting" elements. (time measurement

        o extract "hardware" elements from "fitting" element.

        o apply _resolve_module method to each "hardware" elements. (time measurement

xml files:
    "jeffy_ja-en[99].xml"

NOTE of @decorator:
    o Function to receive arguments of function to be decorated
    o A function that accepts the decorate target function itself as an argument
    o A function that accepts arguments of the decorator itself
"""

class PortUser(IPortUser):

    def on_port_processing(self, action, data=None):
        print(data)
        return True


stpw = Stopwatch('test measurementer')

def test_import_xml():
    usr = PortUser()
# for path in XML_FILES:
    xml_file = "jeffy_ja-en[99].xml"
    fit_count = int(re.search(r"\[(\d+)\]", xml_file).group(1))
    with open(os.path.join(script_dir, xml_file), "r") as file_:
        srcString = file_.read()
        srcString = unicode(srcString, "utf-8")
        #  (basestring, IPortUser, basestring) -> list[eos.saveddata.fit.Fit]
        usr.on_port_process_start()
        stpw.reset()
        with stpw:
            fits = Port.importXml(srcString, usr)

        assert fits is not None and len(fits) is fit_count
