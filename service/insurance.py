import sys
import wx
import threading
from logbook import Logger
from service.esi import Esi

pyfalog = Logger(__name__)


class Insurance():
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Insurance()

        return cls.instance

    def __init__(self):
        self.allInsurance = None

    def apiFetch(self, callerCallback):
        thread = InsuranceApiThread((self.insuranceApiCallback, callerCallback))
        thread.start()

    # Modify the Insurance class with data from the threaded api call if there were no errors
    def insuranceApiCallback(self, response, callerCallback, e=None):
        if e:
            wx.CallAfter(callerCallback, e)
        else:
            self.allInsurance = response
            wx.CallAfter(callerCallback, response)

    def getInsurance(self, typeID):
        if self.allInsurance:
            # Search the insurance list for the first item that has the typeID we are looking for
            try:
                return next(iter([item for item in self.allInsurance if item.get('type_id') == typeID]))['levels']
            except StopIteration:
                return None


class InsuranceApiThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.name = "InsuranceImport"
        self.callback = callback

    def run(self):
        try:
            sEsi = Esi.getInstance()
            resp = sEsi.getInsurance()
            self.callback[0](resp, self.callback[1])
        except Exception as ex:
            pyfalog.warn(ex)
            self.callback[0](None, self.callback[1], sys.exc_info())
